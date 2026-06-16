"""Rolling statistics — all TRAILING (causal): the value at ``t`` uses only data <= ``t``.

``min_periods`` defaults to ``window`` so under-filled early windows are NaN, not fabricated.
Volatility annualizes by ``sqrt(periods_per_year)``; the risk-free rate in rolling Sharpe is annual
and divided by ``periods_per_year`` before subtraction.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .._annualization import ann_factor, infer_periods_per_year
from .._frames import to_tidy, to_wide_values


def _ppy(w: pd.DataFrame, periods_per_year: float | None) -> float:
    if periods_per_year is not None:
        return periods_per_year
    return infer_periods_per_year(pd.DatetimeIndex(w.index))


def rolling_mean(
    returns: pd.DataFrame, window: int, *, min_periods: int | None = None, wide: bool = False
) -> pd.DataFrame:
    w = to_wide_values(returns, wide=wide)
    out = w.rolling(window, min_periods=min_periods or window).mean()
    return out if wide else to_tidy(out, "rolling_mean")


def rolling_vol(
    returns: pd.DataFrame,
    window: int,
    *,
    periods_per_year: float | None = None,
    annualize: bool = True,
    min_periods: int | None = None,
    wide: bool = False,
) -> pd.DataFrame:
    """Rolling standard deviation (ddof=1), annualized by ``sqrt(ppy)`` when ``annualize``."""
    w = to_wide_values(returns, wide=wide)
    out = w.rolling(window, min_periods=min_periods or window).std(ddof=1)
    if annualize:
        out = out * ann_factor(_ppy(w, periods_per_year), vol=True)
    return out if wide else to_tidy(out, "rolling_vol")


def rolling_sharpe(
    returns: pd.DataFrame,
    window: int,
    *,
    rf: float = 0.0,
    periods_per_year: float | None = None,
    min_periods: int | None = None,
    wide: bool = False,
) -> pd.DataFrame:
    """Annualized rolling Sharpe. ``rf`` is an ANNUAL rate, divided by ppy before subtraction."""
    w = to_wide_values(returns, wide=wide)
    ppy = _ppy(w, periods_per_year)
    mp = min_periods or window
    rf_per = rf / ppy
    mean = (w - rf_per).rolling(window, min_periods=mp).mean()
    std = w.rolling(window, min_periods=mp).std(ddof=1)
    out = (mean / std) * ann_factor(ppy, vol=True)
    out = out.replace([np.inf, -np.inf], np.nan)
    return out if wide else to_tidy(out, "rolling_sharpe")


def rolling_zscore(
    series: pd.Series, window: int, *, min_periods: int | None = None
) -> pd.Series:
    """Trailing z-score: ``(x - rolling_mean) / rolling_std`` (ddof=1)."""
    s = pd.Series(series)
    mp = min_periods or window
    mean = s.rolling(window, min_periods=mp).mean()
    std = s.rolling(window, min_periods=mp).std(ddof=1)
    return ((s - mean) / std).replace([np.inf, -np.inf], np.nan).rename("zscore")


def rolling_correlation(
    returns_a: pd.Series, returns_b: pd.Series, window: int, *, min_periods: int | None = None
) -> pd.Series:
    """Pairwise rolling correlation, aligned on the intersection of the two series' dates."""
    a, b = pd.Series(returns_a).align(pd.Series(returns_b), join="inner")
    return a.rolling(window, min_periods=min_periods or window).corr(b).rename("rolling_corr")
