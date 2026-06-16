"""Performance & risk metrics (Sharpe, Sortino, Calmar, drawdown, VaR/CVaR).

Public API (additive within 0.1.x):
    annualize_return, annualize_vol, cagr, sharpe_ratio, sortino_ratio, calmar_ratio
    drawdown_series, underwater_series, max_drawdown, Drawdown, value_at_risk, conditional_var
"""

from __future__ import annotations

from .performance import (
    annualize_return,
    annualize_vol,
    cagr,
    calmar_ratio,
    sharpe_ratio,
    sortino_ratio,
)
from .risk import (
    Drawdown,
    conditional_var,
    drawdown_series,
    max_drawdown,
    underwater_series,
    value_at_risk,
)

__all__ = [
    "annualize_return",
    "annualize_vol",
    "cagr",
    "sharpe_ratio",
    "sortino_ratio",
    "calmar_ratio",
    "drawdown_series",
    "underwater_series",
    "max_drawdown",
    "Drawdown",
    "value_at_risk",
    "conditional_var",
]
