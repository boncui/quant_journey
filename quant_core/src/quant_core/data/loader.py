"""``download_ohlcv`` — the one entry point most projects call to get market data.

Orchestrates provider + cache and returns a canonical tidy frame for the requested
universe and date range. Caching is per-ticker full-history with a TTL (see
:mod:`quant_core.data.cache`); pass ``use_cache=False`` to force a fresh fetch.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from . import cache, schema
from .cache import CacheKey
from .providers import Provider, YFinanceProvider


def download_ohlcv(
    tickers: str | list[str],
    start: str,
    end: str,
    *,
    interval: str = "1d",
    provider: Provider | None = None,
    use_cache: bool = True,
    cache_dir: Path | str = cache.DEFAULT_CACHE_DIR,
    ttl_days: float = 1.0,
) -> pd.DataFrame:
    """Download OHLCV for ``tickers`` over ``[start, end]`` as a canonical tidy frame.

    Each ticker is cached separately as full history; a request is served from cache
    when the cache covers the window and is fresh, otherwise the provider is hit and
    the cache refreshed.
    """
    provider = provider or YFinanceProvider()
    cache_dir = Path(cache_dir)
    ticker_list = [tickers] if isinstance(tickers, str) else list(tickers)

    start_ts = pd.Timestamp(start, tz="UTC")
    end_ts = pd.Timestamp(end, tz="UTC")

    frames: list[pd.DataFrame] = []
    to_fetch: list[str] = []

    for tk in ticker_list:
        key = CacheKey(provider=provider.name, ticker=tk, interval=interval)
        if use_cache:
            cached, fetched_at = cache.load(key, cache_dir)
            if cache.covers(cached, start_ts, end_ts) and not cache.is_stale(fetched_at, ttl_days):
                frames.append(_slice(cached, start_ts, end_ts))
                continue
        to_fetch.append(tk)

    if to_fetch:
        fresh = provider.fetch(to_fetch, start, end, interval=interval)
        fresh = schema.ensure_schema(fresh)
        for tk in to_fetch:
            block = fresh[fresh["ticker"] == tk]
            if use_cache and not block.empty:
                key = CacheKey(provider=provider.name, ticker=tk, interval=interval)
                merged = _merge_history(cache.load(key, cache_dir)[0], block)
                cache.save(merged, key, cache_dir)
            frames.append(_slice(block, start_ts, end_ts))

    if not frames:
        return schema.empty_frame()
    return schema.ensure_schema(pd.concat(frames, ignore_index=True))


def _slice(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    if df.empty:
        return df
    mask = (df["date"] >= start) & (df["date"] <= end)
    return df.loc[mask].copy()


def _merge_history(old: pd.DataFrame | None, new: pd.DataFrame) -> pd.DataFrame:
    """Merge freshly fetched rows over any cached history, newest winning on collisions."""
    if old is None or old.empty:
        return schema.ensure_schema(new)
    combined = pd.concat([old, new], ignore_index=True)
    # Keep the freshly fetched row when a (ticker, date) appears in both.
    combined = combined.drop_duplicates(subset=["ticker", "date"], keep="last")
    return schema.ensure_schema(combined)
