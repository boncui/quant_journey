"""Correlation & covariance across the asset universe (computed on RETURNS, not price levels).

Tidy-long returns are pivoted to a wide matrix internally; ``min_periods`` / dropna alignment keeps
a short-history ticker from poisoning the whole matrix. Covariance annualizes by ``ppy`` (variance
scales linearly with time); correlation is unitless.
"""

from __future__ import annotations

import pandas as pd

from .._annualization import DEFAULT_PERIODS_PER_YEAR, infer_periods_per_year
from .._frames import to_wide_values


def _wide(returns: pd.DataFrame, wide: bool) -> pd.DataFrame:
    return returns if wide else to_wide_values(returns)


def correlation_matrix(
    returns: pd.DataFrame, *, wide: bool = False, method: str = "pearson", min_periods: int | None = None
) -> pd.DataFrame:
    """Ticker x ticker correlation matrix (symmetric, unit diagonal)."""
    w = _wide(returns, wide)
    return w.corr(method=method, min_periods=min_periods or 1)


def covariance_matrix(
    returns: pd.DataFrame,
    *,
    wide: bool = False,
    annualize: bool = False,
    periods_per_year: float | None = None,
    min_periods: int | None = None,
) -> pd.DataFrame:
    """Ticker x ticker covariance matrix; optionally annualized (``cov * ppy``)."""
    w = _wide(returns, wide)
    cov = w.cov(min_periods=min_periods or 1)
    if annualize:
        ppy = periods_per_year
        if ppy is None:
            ppy = infer_periods_per_year(pd.DatetimeIndex(w.index)) if len(w.index) else DEFAULT_PERIODS_PER_YEAR
        cov = cov * ppy
    return cov


def rolling_correlation_matrix(
    returns: pd.DataFrame, window: int, *, wide: bool = False, min_periods: int | None = None
) -> dict[pd.Timestamp, pd.DataFrame]:
    """Map of window-end date -> correlation matrix. Note: O(n_dates) matrices — use a coarse step
    for large universes. For a single pair prefer ``stats.rolling_correlation``."""
    w = _wide(returns, wide)
    mp = min_periods or window
    out: dict[pd.Timestamp, pd.DataFrame] = {}
    for end in range(window - 1, len(w.index)):
        block = w.iloc[max(0, end - window + 1) : end + 1]
        if block.notna().sum().min() >= mp:
            out[w.index[end]] = block.corr()
    return out


def shrink_covariance(returns: pd.DataFrame, *, wide: bool = False, method: str = "ledoit_wolf") -> pd.DataFrame:
    """Shrinkage covariance (stabilizes Phase-3 optimizers). Needs ``quant-core[ml]`` (scikit-learn)."""
    try:
        from sklearn.covariance import OAS, LedoitWolf
    except ModuleNotFoundError as exc:  # pragma: no cover - import guard
        raise ModuleNotFoundError(
            "shrink_covariance() needs scikit-learn. Install the extra: `uv add 'quant-core[ml]'`."
        ) from exc
    w = _wide(returns, wide).dropna()
    estimator = {"ledoit_wolf": LedoitWolf, "oas": OAS}.get(method)
    if estimator is None:
        raise ValueError(f"Unknown shrinkage method: {method!r}")
    cov = estimator().fit(w.to_numpy()).covariance_
    return pd.DataFrame(cov, index=w.columns, columns=w.columns)
