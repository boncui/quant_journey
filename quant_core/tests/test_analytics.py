"""Offline correctness tests for the graduated analytics — closed-form + invariants + edges."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quant_core.factors import beta, capm_fit
from quant_core.metrics import (
    annualize_vol,
    conditional_var,
    max_drawdown,
    sharpe_ratio,
    value_at_risk,
)
from quant_core.portfolio import correlation_matrix
from quant_core.stats import (
    cumulative_returns,
    histogram,
    log_returns,
    moments,
    rolling_mean,
    rolling_vol,
    simple_returns,
)


def _wide(cols: dict[str, list[float]], periods: int) -> pd.DataFrame:
    dates = pd.date_range("2021-01-04", periods=periods, freq="B", tz="UTC")
    return pd.DataFrame(cols, index=pd.DatetimeIndex(dates, name="date"))


# --- returns -----------------------------------------------------------------

def test_log_returns_of_doubling_series():
    w = _wide({"X": [1.0, 2.0, 4.0, 8.0]}, 4)
    r = log_returns(w, wide=True)["X"].dropna().to_numpy()
    assert r == pytest.approx(np.log(2.0))


def test_simple_returns_closed_form():
    w = _wide({"X": [1.0, 2.0, 4.0, 8.0]}, 4)
    r = simple_returns(w, wide=True)["X"].dropna().to_numpy()
    assert r == pytest.approx([1.0, 1.0, 1.0])


def test_log_returns_additive_across_series():
    # invariant: sum of log returns == total log return.
    w = _wide({"X": [1.0, 2.0, 4.0, 8.0, 16.0]}, 5)
    lr = log_returns(w, wide=True)["X"].dropna()
    assert lr.sum() == pytest.approx(np.log(16.0))


def test_cumulative_returns_simple():
    rets = _wide({"X": [np.nan, 0.1, 0.1]}, 3)
    cum = cumulative_returns(rets, wide=True)["X"].to_numpy()
    assert cum == pytest.approx([0.0, 0.1, 0.21])


# --- distribution ------------------------------------------------------------

def test_moments_on_symmetric_sample():
    m = moments(pd.Series([-2.0, -1.0, 0.0, 1.0, 2.0]))
    assert m.n == 5
    assert m.mean == pytest.approx(0.0)
    assert m.std == pytest.approx(np.sqrt(2.5))     # ddof=1
    assert m.skew == pytest.approx(0.0)
    assert m.kurtosis_excess == pytest.approx(-1.3)  # platykurtic


def test_histogram_counts_sum_to_n():
    x = pd.Series(np.random.default_rng(0).normal(size=1000))
    h = histogram(x, bins=10, density=False)
    assert sum(h.counts) == 1000
    assert len(h.bin_centers) == 10


# --- rolling -----------------------------------------------------------------

def test_rolling_mean_trailing():
    rets = _wide({"X": [1.0, 2.0, 3.0, 4.0]}, 4)
    rm = rolling_mean(rets, 2, wide=True)["X"].dropna().to_numpy()
    assert rm == pytest.approx([1.5, 2.5, 3.5])


def test_rolling_vol_constant_series_is_zero():
    rets = _wide({"X": [0.05, 0.05, 0.05, 0.05]}, 4)
    rv = rolling_vol(rets, 2, wide=True, annualize=False)["X"].dropna().to_numpy()
    assert rv == pytest.approx([0.0, 0.0, 0.0])


# --- performance / risk ------------------------------------------------------

def test_annualize_vol_scales_by_sqrt_252():
    r = pd.Series([0.01, -0.02, 0.015, -0.005, 0.02])
    assert annualize_vol(r) == pytest.approx(r.std(ddof=1) * np.sqrt(252))


def test_sharpe_ratio_formula_and_constant_edge():
    r = pd.Series([0.01, -0.01, 0.02, -0.02, 0.03])
    expected = r.mean() / r.std(ddof=1) * np.sqrt(252)
    assert sharpe_ratio(r) == pytest.approx(expected)
    assert np.isnan(sharpe_ratio(pd.Series([0.01] * 5)))  # zero variance


def test_max_drawdown_closed_form():
    eq = pd.Series([1.0, 2.0, 1.0, 2.0], index=pd.date_range("2021-01-04", periods=4, freq="B", tz="UTC"))
    dd = max_drawdown(eq, is_returns=False)
    assert dd.max_drawdown == pytest.approx(-0.5)
    assert dd.recovery_date == eq.index[-1]


def test_var_and_cvar_historical():
    r = pd.Series(np.linspace(-0.1, 0.1, 21))
    q = np.quantile(r.to_numpy(), 0.1)
    assert value_at_risk(r, level=0.9) == pytest.approx(-q)
    tail = r[r <= q]
    assert conditional_var(r, level=0.9) == pytest.approx(-tail.mean())


# --- covariance / beta -------------------------------------------------------

def test_correlation_matrix_identical_and_anti():
    rets = _wide(
        {"A": [0.01, -0.02, 0.03, -0.01], "B": [0.01, -0.02, 0.03, -0.01], "C": [-0.01, 0.02, -0.03, 0.01]},
        4,
    )
    c = correlation_matrix(rets, wide=True)
    assert c.loc["A", "A"] == pytest.approx(1.0)
    assert c.loc["A", "B"] == pytest.approx(1.0)
    assert c.loc["A", "C"] == pytest.approx(-1.0)


def test_beta_and_capm_fit():
    bench = pd.Series([0.01, -0.02, 0.03, -0.01, 0.005])
    asset = 2.0 * bench
    assert beta(asset, bench) == pytest.approx(2.0)
    fit = capm_fit(asset, bench)
    assert fit.beta == pytest.approx(2.0)
    assert fit.r_squared == pytest.approx(1.0)
    assert fit.alpha == pytest.approx(0.0, abs=1e-9)


# --- edges -------------------------------------------------------------------

def test_empty_and_single_row_edges():
    assert moments(pd.Series([], dtype=float)).n == 0
    assert np.isnan(annualize_vol(pd.Series([0.01])))
    one = simple_returns(_wide({"X": [100.0]}, 1), wide=True)
    assert one["X"].dropna().empty


# --- scipy-backed (skip if extra not installed) ------------------------------

def test_normality_and_qq_points():
    pytest.importorskip("scipy")
    from quant_core.stats import normality, qq_points

    r = pd.Series(np.random.default_rng(1).normal(size=500))
    nf = normality(r)
    assert nf.n == 500
    assert 0.0 <= nf.jb_pvalue <= 1.0
    qq = qq_points(r)
    assert len(qq.theoretical) == 500


def test_cluster_order_preserves_membership():
    pytest.importorskip("scipy")
    from quant_core.portfolio import cluster_order

    tickers = ["A", "B", "C", "D"]
    corr = pd.DataFrame(
        [[1.0, 0.9, 0.1, 0.1], [0.9, 1.0, 0.1, 0.1], [0.1, 0.1, 1.0, 0.8], [0.1, 0.1, 0.8, 1.0]],
        index=tickers,
        columns=tickers,
    )
    order = cluster_order(corr)
    assert sorted(order) == sorted(tickers)
