"""Performance metrics on a single return series: annualization, CAGR, Sharpe/Sortino/Calmar.

``periods_per_year`` is inferred from a DatetimeIndex when not given (falls back to 252). The
risk-free rate ``rf`` is annual and converted to per-period internally. CAGR uses *elapsed years*
from the index, so it is robust to gaps and holidays.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .._annualization import DEFAULT_PERIODS_PER_YEAR, ann_factor, infer_periods_per_year
from .risk import max_drawdown


def _ppy(returns: pd.Series, periods_per_year: float | None) -> float:
    if periods_per_year is not None:
        return periods_per_year
    idx = pd.Series(returns).index
    if isinstance(idx, pd.DatetimeIndex):
        return infer_periods_per_year(idx)
    return DEFAULT_PERIODS_PER_YEAR


def annualize_return(returns: pd.Series, *, periods_per_year: float | None = None) -> float:
    """Arithmetic annualized return: ``mean(r) * ppy``."""
    x = pd.Series(returns).dropna()
    if x.empty:
        return float("nan")
    return float(x.mean() * ann_factor(_ppy(returns, periods_per_year), vol=False))


def annualize_vol(returns: pd.Series, *, periods_per_year: float | None = None) -> float:
    """Annualized volatility: ``std(r, ddof=1) * sqrt(ppy)``."""
    x = pd.Series(returns).dropna()
    if len(x) < 2:
        return float("nan")
    return float(x.std(ddof=1) * ann_factor(_ppy(returns, periods_per_year), vol=True))


def cagr(equity_curve: pd.Series) -> float:
    """Geometric annual growth rate from an equity curve, using elapsed calendar years."""
    s = pd.Series(equity_curve).dropna()
    if len(s) < 2 or s.iloc[0] <= 0:
        return float("nan")
    if isinstance(s.index, pd.DatetimeIndex):
        years = (s.index[-1] - s.index[0]).days / 365.25
    else:
        years = (len(s) - 1) / DEFAULT_PERIODS_PER_YEAR
    if years <= 0:
        return float("nan")
    return float((s.iloc[-1] / s.iloc[0]) ** (1.0 / years) - 1.0)


def sharpe_ratio(returns: pd.Series, *, rf: float = 0.0, periods_per_year: float | None = None) -> float:
    """Annualized Sharpe. ``rf`` is annual, divided by ppy before subtraction."""
    x = pd.Series(returns).dropna()
    if len(x) < 2:
        return float("nan")
    ppy = _ppy(returns, periods_per_year)
    excess = x - rf / ppy
    sd = x.std(ddof=1)
    if sd == 0:
        return float("nan")
    return float(excess.mean() / sd * ann_factor(ppy, vol=True))


def sortino_ratio(
    returns: pd.Series, *, rf: float = 0.0, target: float = 0.0, periods_per_year: float | None = None
) -> float:
    """Annualized Sortino. Downside deviation uses only returns < target; denominator over ALL periods."""
    x = pd.Series(returns).dropna()
    if len(x) < 2:
        return float("nan")
    ppy = _ppy(returns, periods_per_year)
    excess = x - rf / ppy
    downside = np.minimum(x - target, 0.0)
    dd = float(np.sqrt((downside**2).mean()))
    if dd == 0:
        return float("nan")
    return float(excess.mean() / dd * ann_factor(ppy, vol=True))


def calmar_ratio(returns: pd.Series, *, periods_per_year: float | None = None) -> float:
    """Annualized return divided by the absolute max drawdown."""
    ann = annualize_return(returns, periods_per_year=periods_per_year)
    mdd = max_drawdown(returns, is_returns=True).max_drawdown
    if mdd == 0 or np.isnan(mdd):
        return float("nan")
    return float(ann / abs(mdd))
