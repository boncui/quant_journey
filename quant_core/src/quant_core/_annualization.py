"""Annualization constants and helpers — the single most error-prone corner of quant math.

Centralizing this means every module agrees on periods-per-year and on the direction of
scaling (mean/return scales by the factor; volatility scales by its square root). Getting
this wrong is the classic Sharpe-ratio bug, so it lives in exactly one place.
"""

from __future__ import annotations

import math

import pandas as pd

#: Trading periods per year by bar interval (financial convention: 252 trading days).
PERIODS_PER_YEAR: dict[str, float] = {
    "1d": 252.0,
    "1wk": 52.0,
    "1mo": 12.0,
    "1h": 252.0 * 6.5,      # ~6.5 trading hours per session
    "30m": 252.0 * 13.0,
    "15m": 252.0 * 26.0,
    "5m": 252.0 * 78.0,
    "1m": 252.0 * 390.0,    # 390 trading minutes per session
}

DEFAULT_PERIODS_PER_YEAR: float = 252.0


def periods_per_year(interval: str) -> float:
    """Look up trading periods/year for a bar ``interval`` (falls back to 252 for daily)."""
    return PERIODS_PER_YEAR.get(interval, DEFAULT_PERIODS_PER_YEAR)


def infer_periods_per_year(index: pd.DatetimeIndex) -> float:
    """Infer trading periods/year from the median spacing of a DatetimeIndex.

    Maps the median delta to the nearest known interval rather than naively dividing a
    calendar year by it (which would mis-annualize daily trading data to 365). Defaults
    to 252 (daily) when the index is too short or ambiguous.
    """
    if index is None or len(index) < 3:
        return DEFAULT_PERIODS_PER_YEAR
    idx = pd.DatetimeIndex(index).sort_values()
    median_days = float(pd.Series(idx).diff().dropna().dt.total_seconds().median()) / 86_400.0
    if median_days <= 0:
        return DEFAULT_PERIODS_PER_YEAR
    if median_days < 0.5 / 24:          # sub-30-minute → treat as minute bars
        return PERIODS_PER_YEAR["1m"]
    if median_days < 0.2:               # intraday hours
        return PERIODS_PER_YEAR["1h"]
    if median_days <= 1.6:              # daily (trading days median ~1, with weekend gaps)
        return PERIODS_PER_YEAR["1d"]
    if median_days <= 10:               # weekly
        return PERIODS_PER_YEAR["1wk"]
    if median_days <= 45:               # monthly
        return PERIODS_PER_YEAR["1mo"]
    return 365.25 / median_days


def ann_factor(ppy: float, *, vol: bool) -> float:
    """Annualization scaling factor.

    ``vol=True`` → ``sqrt(ppy)`` (standard deviations scale with the root of time);
    ``vol=False`` → ``ppy`` (means/returns scale linearly with time).
    """
    return math.sqrt(ppy) if vol else float(ppy)
