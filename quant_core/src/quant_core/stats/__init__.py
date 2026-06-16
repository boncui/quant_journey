"""Statistics: returns, distributions, and rolling windows.

Public API (additive within 0.1.x):
    simple_returns, log_returns, cumulative_returns, resample_returns
    histogram, moments, normality, qq_points, Histogram, Moments, NormalityFit, QQData
    rolling_mean, rolling_vol, rolling_sharpe, rolling_zscore, rolling_correlation
"""

from __future__ import annotations

from .distribution import (
    Histogram,
    Moments,
    NormalityFit,
    QQData,
    histogram,
    moments,
    normality,
    qq_points,
)
from .returns import (
    cumulative_returns,
    log_returns,
    rebased_prices,
    resample_returns,
    simple_returns,
)
from .rolling import (
    rolling_correlation,
    rolling_mean,
    rolling_sharpe,
    rolling_vol,
    rolling_zscore,
)

__all__ = [
    "simple_returns",
    "log_returns",
    "cumulative_returns",
    "rebased_prices",
    "resample_returns",
    "histogram",
    "moments",
    "normality",
    "qq_points",
    "Histogram",
    "Moments",
    "NormalityFit",
    "QQData",
    "rolling_mean",
    "rolling_vol",
    "rolling_sharpe",
    "rolling_zscore",
    "rolling_correlation",
]
