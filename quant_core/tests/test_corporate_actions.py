from __future__ import annotations

import numpy as np
import pytest
from quant_core.data import corporate_actions as ca

from tests.conftest import make_tidy


def test_split_only_does_not_diverge_adjusted_from_raw():
    # yfinance already split-adjusts raw close, so with NO dividends adj_close == close
    # and the adjustment factor is ~1.0 everywhere — a split alone does not diverge.
    dates = ["2021-08-01", "2021-08-02", "2021-08-03", "2021-08-04"]
    df = make_tidy("AAPL", dates, splits={"2021-08-03": 4.0})  # adj_close defaults to == close
    factor = ca.adjustment_factor(df)
    assert np.allclose(factor.to_numpy(), 1.0)
    assert ca.split_dates(df) == [df["date"].iloc[2]]
    assert ca.ex_dividend_dates(df) == []


def test_dividend_only_diverges_adjusted_below_raw_before_exdate():
    # Construct adj_close below close prior to the ex-dividend date (back-adjustment).
    dates = ["2021-08-01", "2021-08-02", "2021-08-03", "2021-08-04"]
    close = np.array([100.0, 101.0, 102.0, 103.0])
    adj = np.array([99.0, 100.0, 102.0, 103.0])  # diverges before the 08-03 ex-date
    df = make_tidy("KO", dates, dividends={"2021-08-03": 1.0}, adj_close=adj)
    # rebuild close to match our explicit array (make_tidy sets close from base+arange)
    df.loc[:, "close"] = close

    factor = ca.adjustment_factor(df)
    assert factor.iloc[0] < 1.0  # adjusted below raw before the dividend
    assert factor.iloc[-1] == pytest.approx(1.0)
    assert ca.ex_dividend_dates(df) == [df["date"].iloc[2]]
    assert ca.split_dates(df) == []


def test_divergence_frame_has_expected_columns():
    df = make_tidy("KO", ["2021-08-01", "2021-08-02"])
    out = ca.divergence(df)
    assert list(out.columns) == ["close", "adj_close", "adj_factor"]


def test_single_ticker_guard_raises_on_multi():
    import pandas as pd

    df = pd.concat([make_tidy("AAPL", ["2021-08-01"]), make_tidy("MSFT", ["2021-08-01"])], ignore_index=True)
    from quant_core.data import schema

    df = schema.ensure_schema(df)
    with pytest.raises(ValueError, match="single ticker"):
        ca.adjustment_factor(df)
