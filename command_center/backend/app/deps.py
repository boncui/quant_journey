"""The single data-access seam. Routes read ONLY through here, so the storage layer can be swapped
(parquet -> duckdb -> stream) without touching any route.

Two on-disk artifact kinds plus an in-memory fallback, kept distinct by ``source``:
- ``cache``        — ~/.cache/quant_journey/ohlcv (raw full history) — the default.
- ``seed``         — backend/.cc_seed (deterministic synthetic, from ``make cc-seed``).
- ``project:NNN``  — NNN_*/data (cleaned, date-bounded slices).
When nothing matches and ``allow_synthetic`` is on, we synthesize in memory so the UI is never blank.
"""

from __future__ import annotations

import pandas as pd
from fastapi import Depends, HTTPException
from quant_core.data import DatasetMeta, build_catalog, make_synthetic_ohlcv, scan_parquet
from quant_core.data.schema import ensure_schema

from .config import Settings, get_settings

# Source precedence when the caller doesn't pin one: full-history cache > synthetic seed > project slice.
_SOURCE_RANK = {"cache": 0, "seed": 1}


def get_catalog(settings: Settings = Depends(get_settings)) -> list[DatasetMeta]:
    """Enumerate all datasets: monorepo project slices + the cache + the synthetic seed dir."""
    metas = build_catalog(settings.repo_root, cache_dir=settings.cache_dir)
    if settings.seed_dir.is_dir():
        for path in sorted(settings.seed_dir.glob("*.parquet")):
            try:
                metas.append(scan_parquet(path, "seed"))
            except Exception:
                continue
    return metas


def _rank(meta: DatasetMeta) -> int:
    if meta.source.startswith("project:"):
        return 2
    return _SOURCE_RANK.get(meta.source, 3)


def resolve_dataset(
    catalog: list[DatasetMeta], ticker: str, *, interval: str | None = "1d", source: str | None = None
) -> DatasetMeta | None:
    """Resolve ticker -> dataset via the in-memory catalog ONLY (never build a path from user input)."""
    candidates = [
        m
        for m in catalog
        if ticker in m.tickers
        and (source is None or m.source == source)
        and (interval is None or m.interval is None or m.interval == interval)
    ]
    if not candidates:
        return None
    return sorted(candidates, key=_rank)[0]


def load_ohlcv(
    settings: Settings,
    catalog: list[DatasetMeta],
    ticker: str,
    *,
    start: str | None = None,
    end: str | None = None,
    interval: str = "1d",
    source: str | None = None,
) -> pd.DataFrame:
    """Canonical tidy OHLCV for one ticker over [start, end]. Synthesizes if nothing matches."""
    meta = resolve_dataset(catalog, ticker, interval=interval, source=source)
    if meta is not None:
        df = ensure_schema(pd.read_parquet(meta.path))
        df = df[df["ticker"] == ticker]
    elif settings.allow_synthetic:
        df = make_synthetic_ohlcv([ticker], settings.default_start, settings.default_end, interval=interval)
    else:
        raise HTTPException(status_code=404, detail=f"No data for ticker {ticker!r}.")

    if start:
        df = df[df["date"] >= pd.Timestamp(start, tz="UTC")]
    if end:
        df = df[df["date"] <= pd.Timestamp(end, tz="UTC")]
    return df.sort_values("date").reset_index(drop=True)
