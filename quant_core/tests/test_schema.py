from __future__ import annotations

import pandas as pd
import pytest
from quant_core.data import schema

from tests.conftest import make_tidy


def test_empty_frame_has_canonical_columns_and_dtypes():
    df = schema.empty_frame()
    assert list(df.columns) == schema.OHLCV_COLUMNS
    assert df.empty
    assert str(df["date"].dtype) == "datetime64[ns, UTC]"
    assert isinstance(df["ticker"].dtype, pd.CategoricalDtype)


def test_ensure_schema_localizes_naive_dates_to_utc():
    raw = pd.DataFrame(
        {
            "date": pd.to_datetime(["2021-01-04", "2021-01-05"]),  # tz-naive
            "ticker": "AAPL",
            "open": [1.0, 2.0],
            "high": [2.0, 3.0],
            "low": [0.5, 1.5],
            "close": [1.5, 2.5],
            "adj_close": [1.5, 2.5],
            "volume": [10.0, 20.0],
        }
    )
    out = schema.ensure_schema(raw)
    assert str(out["date"].dtype) == "datetime64[ns, UTC]"
    assert (out["dividends"] == 0.0).all()  # filled
    assert (out["splits"] == 0.0).all()


def test_ensure_schema_missing_required_column_raises():
    bad = pd.DataFrame({"date": pd.to_datetime(["2021-01-04"]), "ticker": ["AAPL"]})
    with pytest.raises(ValueError, match="missing required columns"):
        schema.ensure_schema(bad)


def test_to_wide_and_back_roundtrips_adj_close():
    dates = ["2021-06-01", "2021-06-02", "2021-06-03"]
    df = pd.concat(
        [make_tidy("AAPL", dates, close_base=100.0), make_tidy("MSFT", dates, close_base=200.0)],
        ignore_index=True,
    )
    df = schema.ensure_schema(df)
    wide = schema.to_wide(df, field="adj_close")
    assert list(wide.columns) == ["AAPL", "MSFT"]
    assert len(wide) == 3
    back = schema.from_wide(wide, field="adj_close")
    merged = df.merge(back, on=["date", "ticker"], suffixes=("", "_back"))
    assert (merged["adj_close"] == merged["adj_close_back"]).all()


def test_to_wide_empty_is_empty():
    assert schema.to_wide(schema.empty_frame()).empty
