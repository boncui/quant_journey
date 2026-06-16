from __future__ import annotations

import pytest
from quant_core.data import schema
from quant_core.data.providers import PolygonProvider, normalize_yfinance


def test_normalize_single_ticker_flat_columns(raw_yf_single):
    tidy = normalize_yfinance(raw_yf_single, ["AAPL"])
    assert list(tidy.columns) == schema.OHLCV_COLUMNS
    assert set(tidy["ticker"].unique()) == {"AAPL"}
    assert len(tidy) == len(raw_yf_single)
    assert str(tidy["date"].dtype) == "datetime64[ns, UTC]"


def test_normalize_multi_ticker_multiindex_columns(raw_yf_multi):
    tidy = normalize_yfinance(raw_yf_multi, ["AAPL", "MSFT"])
    assert set(tidy["ticker"].unique()) == {"AAPL", "MSFT"}
    # MSFT base is 200, AAPL base is 100 — sanity that columns weren't crossed.
    assert tidy.loc[tidy["ticker"] == "MSFT", "close"].iloc[0] == pytest.approx(200.0)
    assert tidy.loc[tidy["ticker"] == "AAPL", "close"].iloc[0] == pytest.approx(100.0)


def test_normalize_missing_adj_close_raises(raw_yf_no_adjclose):
    with pytest.raises(ValueError, match="No 'Adj Close'"):
        normalize_yfinance(raw_yf_no_adjclose, ["AAPL"])


def test_normalize_empty_returns_empty_frame():
    import pandas as pd

    out = normalize_yfinance(pd.DataFrame(), ["AAPL"])
    assert out.empty
    assert list(out.columns) == schema.OHLCV_COLUMNS


def test_polygon_stub_not_implemented():
    with pytest.raises(NotImplementedError):
        PolygonProvider(api_key="x").fetch(["AAPL"], "2021-01-01", "2021-02-01")
