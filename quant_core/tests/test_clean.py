from __future__ import annotations

import pandas as pd
from quant_core.data.clean import clean_ohlcv

from tests.conftest import make_tidy


def test_nyse_holiday_is_not_a_gap():
    # July 5 2021 = observed Independence Day (NYSE closed). July 2 (Fri), 6 (Tue), 7 (Wed) trade.
    df = make_tidy("AAPL", ["2021-07-02", "2021-07-06", "2021-07-07"])
    _, report = clean_ohlcv(df, calendar="NYSE")
    r = report.per_ticker["AAPL"]
    assert r.n_missing == 0, f"holiday wrongly flagged as gap: {r.missing_sessions}"


def test_real_missing_trading_day_is_detected():
    # Omit 2021-07-06, a genuine NYSE session, between two present sessions.
    df = make_tidy("AAPL", ["2021-07-02", "2021-07-07"])
    _, report = clean_ohlcv(df, calendar="NYSE")
    r = report.per_ticker["AAPL"]
    assert r.n_missing == 1
    assert pd.Timestamp("2021-07-06", tz="UTC") in r.missing_sessions


def test_validation_flags_high_low_inversion():
    df = make_tidy("AAPL", ["2021-06-01", "2021-06-02", "2021-06-03"])
    # Corrupt one row so high < low.
    df.loc[1, "high"] = df.loc[1, "low"] - 5.0
    _, report = clean_ohlcv(df, calendar="NYSE")
    assert report.per_ticker["AAPL"].n_validation_violations == 1


def test_ffill_reindexes_missing_session():
    df = make_tidy("AAPL", ["2021-07-02", "2021-07-07"])  # missing 07-06
    clean, report = clean_ohlcv(df, calendar="NYSE", fill="ffill")
    # 07-06 should now exist, forward-filled, with volume 0.
    filled = clean[clean["date"] == pd.Timestamp("2021-07-06", tz="UTC")]
    assert len(filled) == 1
    assert filled["volume"].iloc[0] == 0.0


def test_empty_input_is_handled():
    from quant_core.data import schema

    clean, report = clean_ohlcv(schema.empty_frame())
    assert clean.empty
    assert report.total_missing == 0
