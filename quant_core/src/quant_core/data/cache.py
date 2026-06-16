"""On-disk OHLCV cache (parquet), one file per (provider, ticker, interval).

Design notes (these matter for data integrity, per the roadmap's rigor emphasis):

- We cache the **full fetched history** for a ticker, not a per-request range. A request
  for a sub-range is served by slicing; only genuinely missing spans trigger a fetch.
- A ``fetched_at`` timestamp + TTL handles the fact that yfinance **retroactively
  revises** history when a new split/dividend occurs (back-adjustment rewrites the
  whole Adj Close series). A stale cache is refetched rather than silently served.
- The cache key includes the provider, ticker and interval so a daily cache is never
  served for a request that wanted something else. (auto_adjust is fixed to False
  across the library, so it is not part of the key.)
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from . import schema

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "quant_journey" / "ohlcv"


@dataclass(frozen=True)
class CacheKey:
    provider: str
    ticker: str
    interval: str

    def hash(self) -> str:
        raw = f"{self.provider}|{self.ticker}|{self.interval}".encode()
        return hashlib.sha1(raw).hexdigest()[:16]


def _paths(cache_dir: Path, key: CacheKey) -> tuple[Path, Path]:
    base = cache_dir / f"{key.ticker}_{key.interval}_{key.hash()}"
    return base.with_suffix(".parquet"), base.with_suffix(".meta.json")


def load(key: CacheKey, cache_dir: Path = DEFAULT_CACHE_DIR) -> tuple[pd.DataFrame | None, datetime | None]:
    """Load cached full history for a key. Returns ``(df_or_None, fetched_at_or_None)``."""
    parquet_path, meta_path = _paths(Path(cache_dir), key)
    if not parquet_path.exists():
        return None, None
    df = schema.ensure_schema(pd.read_parquet(parquet_path))
    fetched_at: datetime | None = None
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        ts = meta.get("fetched_at")
        if ts:
            fetched_at = datetime.fromisoformat(ts)
    return df, fetched_at


def save(
    df: pd.DataFrame,
    key: CacheKey,
    cache_dir: Path = DEFAULT_CACHE_DIR,
    fetched_at: datetime | None = None,
) -> None:
    """Persist the full history for a key plus its ``fetched_at`` metadata sidecar."""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    parquet_path, meta_path = _paths(cache_dir, key)
    schema.ensure_schema(df).to_parquet(parquet_path, index=False)
    fetched_at = fetched_at or datetime.now(timezone.utc)
    meta_path.write_text(json.dumps({"fetched_at": fetched_at.isoformat()}))


def is_stale(fetched_at: datetime | None, ttl_days: float = 1.0) -> bool:
    """True if there is no timestamp or it is older than ``ttl_days``."""
    if fetched_at is None:
        return True
    age = datetime.now(timezone.utc) - fetched_at
    return age.total_seconds() > ttl_days * 86_400


def covers(df: pd.DataFrame | None, start: pd.Timestamp, end: pd.Timestamp) -> bool:
    """True if cached ``df`` spans the whole requested ``[start, end]`` window."""
    if df is None or df.empty:
        return False
    return df["date"].min() <= start and df["date"].max() >= end
