from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pandas as pd
from quant_core.data import cache
from quant_core.data.cache import CacheKey
from quant_core.data.loader import download_ohlcv

from tests.conftest import FakeProvider, make_tidy

DATES = ["2021-06-01", "2021-06-02", "2021-06-03", "2021-06-04", "2021-06-07"]


def test_cache_round_trip(tmp_path):
    df = make_tidy("AAPL", DATES)
    key = CacheKey(provider="fake", ticker="AAPL", interval="1d")
    cache.save(df, key, tmp_path)
    loaded, fetched_at = cache.load(key, tmp_path)
    assert loaded is not None and len(loaded) == len(df)
    assert isinstance(fetched_at, datetime)


def test_is_stale_and_covers(tmp_path):
    df = make_tidy("AAPL", DATES)
    assert cache.is_stale(None)
    assert cache.is_stale(datetime.now(UTC) - timedelta(days=3), ttl_days=1)
    assert not cache.is_stale(datetime.now(UTC), ttl_days=1)
    assert cache.covers(df, pd.Timestamp("2021-06-02", tz="UTC"), pd.Timestamp("2021-06-03", tz="UTC"))
    assert not cache.covers(df, pd.Timestamp("2021-05-01", tz="UTC"), pd.Timestamp("2021-06-03", tz="UTC"))


def test_loader_fetches_then_serves_from_cache(tmp_path):
    provider = FakeProvider({"AAPL": make_tidy("AAPL", DATES)})
    out1 = download_ohlcv("AAPL", "2021-06-01", "2021-06-07", provider=provider, cache_dir=tmp_path)
    assert len(out1) == 5
    assert len(provider.calls) == 1  # fetched once

    # Second call for a sub-range is served from cache (no new fetch).
    out2 = download_ohlcv("AAPL", "2021-06-02", "2021-06-04", provider=provider, cache_dir=tmp_path)
    assert len(out2) == 3
    assert len(provider.calls) == 1, "sub-range should be served from cache, not refetched"


def test_loader_use_cache_false_always_fetches(tmp_path):
    provider = FakeProvider({"AAPL": make_tidy("AAPL", DATES)})
    download_ohlcv("AAPL", "2021-06-01", "2021-06-07", provider=provider, cache_dir=tmp_path, use_cache=False)
    download_ohlcv("AAPL", "2021-06-01", "2021-06-07", provider=provider, cache_dir=tmp_path, use_cache=False)
    assert len(provider.calls) == 2


def test_loader_multi_ticker(tmp_path):
    provider = FakeProvider(
        {"AAPL": make_tidy("AAPL", DATES, close_base=100.0), "MSFT": make_tidy("MSFT", DATES, close_base=200.0)}
    )
    out = download_ohlcv(["AAPL", "MSFT"], "2021-06-01", "2021-06-07", provider=provider, cache_dir=tmp_path)
    assert set(out["ticker"].unique()) == {"AAPL", "MSFT"}
    assert len(out) == 10


def test_loader_unknown_ticker_returns_empty(tmp_path):
    provider = FakeProvider({})
    out = download_ohlcv("NOPE", "2021-06-01", "2021-06-07", provider=provider, cache_dir=tmp_path)
    assert out.empty
