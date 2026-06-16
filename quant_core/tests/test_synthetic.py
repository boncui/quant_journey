"""Synthetic OHLCV: canonical schema, determinism, OHLC sanity, and the planted correlation."""

from __future__ import annotations

import pandas as pd
import pytest
from quant_core.data import OHLCV_COLUMNS, make_synthetic_ohlcv
from quant_core.portfolio import correlation_matrix
from quant_core.stats import log_returns


def test_schema_and_determinism():
    a = make_synthetic_ohlcv(["SPY", "KO"], "2020-01-01", "2021-01-01", seed=3)
    b = make_synthetic_ohlcv(["SPY", "KO"], "2020-01-01", "2021-01-01", seed=3)
    assert list(a.columns) == OHLCV_COLUMNS
    pd.testing.assert_frame_equal(a, b)
    assert str(a["date"].dtype) == "datetime64[ns, UTC]"


def test_ohlc_sanity():
    df = make_synthetic_ohlcv(["AAPL"], "2020-01-01", "2021-01-01", seed=5)
    assert (df["high"] >= df["low"]).all()
    assert (df["high"] >= df["close"]).all()
    assert (df["low"] <= df["close"]).all()
    assert (df[["open", "high", "low", "close", "adj_close"]] > 0).all().all()


def test_adj_close_diverges_from_dividends():
    df = make_synthetic_ohlcv(["KO"], "2018-01-01", "2023-01-01", seed=9, annual_dividend_yield=0.03)
    # back-adjustment makes adj_close <= close before the final ex-date; they converge at the end.
    assert (df["adj_close"] <= df["close"] + 1e-9).all()
    assert df["adj_close"].iloc[-1] == pytest.approx(df["close"].iloc[-1])
    assert (df["dividends"] > 0).any()


def test_planted_market_factor_correlation_is_positive():
    df = make_synthetic_ohlcv(["SPY", "KO", "AAPL"], "2018-01-01", "2023-01-01", seed=11)
    corr = correlation_matrix(log_returns(df))
    assert corr.loc["SPY", "KO"] > 0.2
    assert corr.loc["SPY", "AAPL"] > 0.2
    for tk in ("SPY", "KO", "AAPL"):
        assert corr.loc[tk, tk] == pytest.approx(1.0)
