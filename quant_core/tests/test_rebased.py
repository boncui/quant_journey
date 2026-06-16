"""rebased_prices: every series starts exactly at the base and equals base * p/p0."""

from __future__ import annotations

import pandas as pd
import pytest
from quant_core.stats import rebased_prices


def _wide(cols, periods):
    dates = pd.date_range("2021-01-04", periods=periods, freq="B", tz="UTC")
    return pd.DataFrame(cols, index=pd.DatetimeIndex(dates, name="date"))


def test_rebased_starts_at_base_and_tracks_ratio():
    w = _wide({"X": [50.0, 75.0, 100.0], "Y": [10.0, 20.0, 5.0]}, 3)
    rb = rebased_prices(w, base=100.0, wide=True)
    assert rb["X"].to_numpy() == pytest.approx([100.0, 150.0, 200.0])
    assert rb["Y"].to_numpy() == pytest.approx([100.0, 200.0, 50.0])


def test_rebased_tidy_first_point_is_base():
    from quant_core.data import make_synthetic_ohlcv

    df = make_synthetic_ohlcv(["SPY", "KO"], "2020-01-01", "2020-06-01", seed=2)
    rb = rebased_prices(df, base=100.0)
    for t in ("SPY", "KO"):
        sub = rb[rb["ticker"] == t].sort_values("date")
        assert sub["rebased"].iloc[0] == pytest.approx(100.0)
