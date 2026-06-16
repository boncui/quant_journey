"""Catalog/discovery — enumerate every OHLCV dataset across the monorepo, cheaply.

The command_center catalog panel is the front door: it lists what data exists without loading
any frames. Two kinds of artifact coexist and are kept **distinct** (never merged) because they
mean different things for the same ticker:

- ``project:NNN`` — ``NNN_*/data/{ticker}_{interval}.parquet``: a *cleaned, date-bounded slice*
  a project wrote.
- ``cache`` — ``~/.cache/quant_journey/ohlcv/{ticker}_{interval}_{hash}.parquet``: the *raw full
  history* the loader caches.

Scanning is O(metadata): pyarrow row-group statistics give the date span with zero row reads when
available (with a guarded fallback to reading just the ``date`` column). Sizes/counts come from the
parquet footer. Tickers come from the (tiny, categorical) ``ticker`` column.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from .cache import DEFAULT_CACHE_DIR
from .clean import expected_sessions


@dataclass(frozen=True)
class DatasetMeta:
    """Cheap, load-free description of one parquet dataset."""

    path: Path
    source: str                       # "project:001_market_data_downloader_cleaner" | "cache"
    tickers: list[str]
    interval: str | None
    n_rows: int
    n_bytes: int
    start: pd.Timestamp | None
    end: pd.Timestamp | None
    modified_at: datetime
    provider: str | None = None
    fetched_at: datetime | None = None   # cache freshness, from the .meta.json sidecar


@dataclass(frozen=True)
class CoverageReport:
    """Per-ticker gap/freshness vs an exchange calendar."""

    ticker: str
    interval: str
    start: pd.Timestamp
    end: pd.Timestamp
    n_present: int
    n_expected: int
    missing_pct: float
    last_session_gap: int             # trading sessions between `end` and `asof`
    missing_sessions: list[pd.Timestamp] = field(default_factory=list)


def discover_roots(
    repo_root: Path | str,
    *,
    cache_dir: Path | str = DEFAULT_CACHE_DIR,
) -> list[tuple[Path, str]]:
    """Return ``(directory, source_label)`` pairs to scan: every ``NNN_*/data`` + the cache dir."""
    repo_root = Path(repo_root)
    roots: list[tuple[Path, str]] = []
    for data_dir in sorted(repo_root.glob("[0-9][0-9][0-9]_*/data")):
        if data_dir.is_dir():
            roots.append((data_dir, f"project:{data_dir.parent.name}"))
    cache_dir = Path(cache_dir)
    if cache_dir.is_dir():
        roots.append((cache_dir, "cache"))
    return roots


def _date_span(pf: pq.ParquetFile, path: Path) -> tuple[pd.Timestamp | None, pd.Timestamp | None]:
    """Date span from row-group statistics when present; else read just the ``date`` column."""
    try:
        names = pf.schema_arrow.names
        if "date" not in names:
            return None, None
        col = names.index("date")
        mins: list = []
        maxs: list = []
        ok = pf.metadata.num_row_groups > 0
        for rg in range(pf.metadata.num_row_groups):
            stats = pf.metadata.row_group(rg).column(col).statistics
            if stats is None or not stats.has_min_max:
                ok = False
                break
            mins.append(stats.min)
            maxs.append(stats.max)
        if ok and mins:
            return pd.Timestamp(min(mins)), pd.Timestamp(max(maxs))
    except Exception:
        pass
    # Fallback: read only the date column (still far cheaper than the whole frame).
    dates = pd.to_datetime(pq.read_table(path, columns=["date"]).column("date").to_pandas())
    if len(dates) == 0:
        return None, None
    return pd.Timestamp(dates.min()), pd.Timestamp(dates.max())


def _normalize_ts(ts: pd.Timestamp | None) -> pd.Timestamp | None:
    if ts is None or pd.isna(ts):
        return None
    ts = pd.Timestamp(ts)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def scan_parquet(path: Path | str, source: str) -> DatasetMeta:
    """Describe one parquet file without loading its rows."""
    path = Path(path)
    pf = pq.ParquetFile(path)
    n_rows = pf.metadata.num_rows
    start, end = _date_span(pf, path)

    tickers: list[str] = []
    if "ticker" in pf.schema_arrow.names:
        tk = pq.read_table(path, columns=["ticker"]).column("ticker").to_pandas()
        tickers = sorted(map(str, pd.unique(tk.dropna())))

    # Filename convention: "{ticker}_{interval}[...].parquet".
    interval: str | None = None
    stem_parts = path.stem.split("_")
    if len(stem_parts) >= 2:
        interval = stem_parts[1]

    provider: str | None = None
    fetched_at: datetime | None = None
    meta_path = path.with_suffix(".meta.json")
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
            ts = meta.get("fetched_at")
            fetched_at = datetime.fromisoformat(ts) if ts else None
        except Exception:
            fetched_at = None
    if source == "cache":
        provider = "cache"

    st = path.stat()
    return DatasetMeta(
        path=path,
        source=source,
        tickers=tickers,
        interval=interval,
        n_rows=n_rows,
        n_bytes=st.st_size,
        start=_normalize_ts(start),
        end=_normalize_ts(end),
        modified_at=datetime.fromtimestamp(st.st_mtime, tz=timezone.utc),
        provider=provider,
        fetched_at=fetched_at,
    )


def build_catalog(
    repo_root: Path | str,
    *,
    cache_dir: Path | str = DEFAULT_CACHE_DIR,
) -> list[DatasetMeta]:
    """Enumerate all OHLCV parquet datasets across projects + the cache (no full-frame loads)."""
    out: list[DatasetMeta] = []
    for directory, source in discover_roots(repo_root, cache_dir=cache_dir):
        for path in sorted(directory.glob("*.parquet")):
            try:
                out.append(scan_parquet(path, source))
            except Exception:
                # A corrupt/partial file should not sink the whole catalog; skip it.
                continue
    return out


def coverage(
    meta: DatasetMeta,
    *,
    calendar: str = "NYSE",
    asof: pd.Timestamp | None = None,
) -> list[CoverageReport]:
    """Per-ticker gap/freshness for one dataset, vs the exchange trading calendar."""
    if meta.start is None or meta.end is None:
        return []
    frame = pq.read_table(meta.path, columns=["date", "ticker"]).to_pandas()
    frame["date"] = pd.to_datetime(frame["date"], utc=True).dt.normalize()
    asof = pd.Timestamp(asof, tz="UTC").normalize() if asof is not None else None

    reports: list[CoverageReport] = []
    for ticker, block in frame.groupby("ticker", observed=True):
        present = pd.DatetimeIndex(block["date"].unique())
        lo, hi = present.min(), present.max()
        sessions = expected_sessions(lo, hi, calendar=calendar)
        missing = sessions.difference(present)
        n_expected = len(sessions)
        gap = 0
        if asof is not None and asof > hi:
            gap = max(0, len(expected_sessions(hi, asof, calendar=calendar)) - 1)
        reports.append(
            CoverageReport(
                ticker=str(ticker),
                interval=meta.interval or "1d",
                start=_normalize_ts(lo),
                end=_normalize_ts(hi),
                n_present=len(present),
                n_expected=n_expected,
                missing_pct=(len(missing) / n_expected * 100.0) if n_expected else 0.0,
                last_session_gap=gap,
                missing_sessions=list(missing),
            )
        )
    return reports
