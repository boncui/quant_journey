"""CAPM beta/alpha vs a benchmark, plus rolling beta.

All estimates use the INNER-JOIN intersection of the asset and benchmark dates (a misaligned shift
fabricates beta). The risk-free rate is annual and converted per-period; the same per-period rf is
subtracted from both legs before regressing.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .._annualization import DEFAULT_PERIODS_PER_YEAR, ann_factor, infer_periods_per_year


@dataclass(frozen=True)
class CAPMFit:
    alpha: float          # annualized Jensen's alpha
    beta: float
    r_squared: float
    n: int


def _ppy(index, periods_per_year: float | None) -> float:
    if periods_per_year is not None:
        return periods_per_year
    if isinstance(index, pd.DatetimeIndex):
        return infer_periods_per_year(index)
    return DEFAULT_PERIODS_PER_YEAR


def _aligned(asset: pd.Series, benchmark: pd.Series) -> tuple[pd.Series, pd.Series]:
    a, b = pd.Series(asset).align(pd.Series(benchmark), join="inner")
    mask = a.notna() & b.notna()
    return a[mask], b[mask]


def beta(asset_returns: pd.Series, benchmark_returns: pd.Series) -> float:
    """``cov(asset, benchmark) / var(benchmark)`` on the aligned intersection."""
    a, b = _aligned(asset_returns, benchmark_returns)
    if len(a) < 2:
        return float("nan")
    var_b = float(b.var(ddof=1))
    if var_b == 0:
        return float("nan")
    return float(a.cov(b) / var_b)


def capm_fit(asset_returns: pd.Series, benchmark_returns: pd.Series, *, rf: float = 0.0,
             periods_per_year: float | None = None) -> CAPMFit:
    """OLS CAPM fit (numpy lstsq): annualized alpha, beta, R², n."""
    a, b = _aligned(asset_returns, benchmark_returns)
    n = len(a)
    if n < 2:
        return CAPMFit(alpha=float("nan"), beta=float("nan"), r_squared=float("nan"), n=n)
    ppy = _ppy(a.index, periods_per_year)
    rf_per = rf / ppy
    y = (a - rf_per).to_numpy()
    x = (b - rf_per).to_numpy()
    X = np.column_stack([np.ones(n), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    intercept, slope = float(coef[0]), float(coef[1])
    resid = y - X @ coef
    ss_res = float((resid**2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return CAPMFit(alpha=intercept * ann_factor(ppy, vol=False), beta=slope, r_squared=r2, n=n)


def alpha(asset_returns: pd.Series, benchmark_returns: pd.Series, *, rf: float = 0.0,
          periods_per_year: float | None = None) -> float:
    """Annualized Jensen's alpha from the CAPM fit."""
    return capm_fit(asset_returns, benchmark_returns, rf=rf, periods_per_year=periods_per_year).alpha


def rolling_beta(asset_returns: pd.Series, benchmark_returns: pd.Series, window: int, *,
                 min_periods: int | None = None) -> pd.Series:
    """Trailing rolling beta = ``rolling_cov(a, b) / rolling_var(b)``."""
    a, b = _aligned(asset_returns, benchmark_returns)
    mp = min_periods or window
    cov = a.rolling(window, min_periods=mp).cov(b)
    var = b.rolling(window, min_periods=mp).var(ddof=1)
    return (cov / var).replace([np.inf, -np.inf], np.nan).rename("rolling_beta")
