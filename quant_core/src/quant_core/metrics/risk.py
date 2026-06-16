"""Risk metrics: drawdown, Value-at-Risk, Expected Shortfall.

Conventions fixed here so callers (and future v2 panels) are stable:
- Drawdown is computed on an EQUITY curve (returns are converted internally) and is <= 0.
- VaR/CVaR return a **positive loss magnitude**; ``level=0.95`` means the 5% left tail.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Drawdown:
    max_drawdown: float            # <= 0
    peak_date: pd.Timestamp | None
    trough_date: pd.Timestamp | None
    recovery_date: pd.Timestamp | None
    duration: int                  # observations from peak to trough


def _equity(series: pd.Series, *, is_returns: bool) -> pd.Series:
    s = pd.Series(series).dropna()
    if not is_returns:
        return s
    return (1.0 + s).cumprod()


def drawdown_series(series: pd.Series, *, is_returns: bool = True) -> pd.Series:
    """Drawdown path ``equity / running_peak - 1`` (<= 0), indexed like the input."""
    equity = _equity(series, is_returns=is_returns)
    if equity.empty:
        return equity
    return (equity / equity.cummax() - 1.0).rename("drawdown")


def underwater_series(series: pd.Series, *, is_returns: bool = True) -> pd.Series:
    """Alias of :func:`drawdown_series`, named for the underwater plot."""
    return drawdown_series(series, is_returns=is_returns).rename("underwater")


def max_drawdown(series: pd.Series, *, is_returns: bool = True) -> Drawdown:
    """Maximum drawdown plus peak/trough/recovery dates and duration."""
    dd = drawdown_series(series, is_returns=is_returns)
    if dd.empty:
        return Drawdown(max_drawdown=0.0, peak_date=None, trough_date=None, recovery_date=None, duration=0)
    trough = dd.idxmin()
    mdd = float(dd.loc[trough])
    equity = _equity(series, is_returns=is_returns)
    peak = equity.loc[:trough].idxmax()
    after = equity.loc[trough:]
    peak_level = equity.loc[peak]
    recovered = after[after >= peak_level]
    recovery = recovered.index[0] if len(recovered) else None
    duration = int(equity.index.get_loc(trough) - equity.index.get_loc(peak))
    return Drawdown(max_drawdown=mdd, peak_date=peak, trough_date=trough, recovery_date=recovery, duration=duration)


def value_at_risk(returns: pd.Series, *, level: float = 0.95, method: str = "historical") -> float:
    """VaR as a positive loss. ``level=0.95`` -> 5% tail. methods: historical|gaussian|cornish_fisher."""
    x = pd.Series(returns).dropna().to_numpy(dtype=float)
    if x.size == 0:
        return float("nan")
    alpha = 1.0 - level
    if method == "historical":
        return float(-np.quantile(x, alpha))
    try:
        from scipy import stats as ss
    except ModuleNotFoundError as exc:  # pragma: no cover - import guard
        raise ModuleNotFoundError(
            f"VaR method '{method}' needs scipy. Install `quant-core[stats]` or use method='historical'."
        ) from exc
    mu, sigma = float(x.mean()), float(x.std(ddof=1))
    z = ss.norm.ppf(alpha)
    if method == "gaussian":
        return float(-(mu + sigma * z))
    if method == "cornish_fisher":
        s = float(ss.skew(x))
        k = float(ss.kurtosis(x))  # excess
        z_cf = z + (z**2 - 1) * s / 6 + (z**3 - 3 * z) * k / 24 - (2 * z**3 - 5 * z) * s**2 / 36
        return float(-(mu + sigma * z_cf))
    raise ValueError(f"Unknown VaR method: {method!r}")


def conditional_var(returns: pd.Series, *, level: float = 0.95, method: str = "historical") -> float:
    """Expected Shortfall: mean loss beyond VaR, as a positive number. Historical only for now."""
    x = pd.Series(returns).dropna().to_numpy(dtype=float)
    if x.size == 0:
        return float("nan")
    if method != "historical":
        raise ValueError("conditional_var currently supports method='historical'.")
    q = np.quantile(x, 1.0 - level)
    tail = x[x <= q]
    if tail.size == 0:
        return float(-q)
    return float(-tail.mean())
