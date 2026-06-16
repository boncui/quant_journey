"""Return conventions: simple vs log, cumulative growth, and resampling.

Returns are computed **per ticker** (pivot to wide first, so each column is an independent series
and one ticker's first observation is never computed off another's last — no cross-ticker leak).
Simple and log returns are never mixed: simple compounds multiplicatively, log additively.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .._frames import to_tidy, to_wide_values
from ..data.schema import to_wide


def _prices_wide(prices: pd.DataFrame, field: str, wide: bool) -> pd.DataFrame:
    return prices if wide else to_wide(prices, field=field)


def simple_returns(
    prices: pd.DataFrame, *, field: str = "adj_close", wide: bool = False
) -> pd.DataFrame:
    """Simple returns ``p_t / p_{t-1} - 1``. Tidy OHLCV in -> tidy ``[date, ticker, ret]``;
    wide price matrix in (``wide=True``) -> wide returns. First obs per ticker is dropped."""
    w = _prices_wide(prices, field, wide).pct_change()
    return w if wide else to_tidy(w, "ret")


def log_returns(
    prices: pd.DataFrame, *, field: str = "adj_close", wide: bool = False
) -> pd.DataFrame:
    """Log returns ``ln(p_t / p_{t-1})``. Same shape contract as :func:`simple_returns`."""
    pw = _prices_wide(prices, field, wide)
    w = np.log(pw / pw.shift(1))
    return w if wide else to_tidy(w, "ret")


def cumulative_returns(
    returns: pd.DataFrame, *, log: bool = False, wide: bool = False
) -> pd.DataFrame:
    """Cumulative return (growth of the series, 0 at the start).

    ``log=False`` (simple): ``(1 + r).cumprod() - 1``. ``log=True``: ``expm1(r.cumsum())``.
    Missing returns are treated as 0 (no change) so the path starts cleanly at 0 — suitable for a
    rebased overlay (the panel renders ``100 * (1 + cumret)``).
    """
    w = to_wide_values(returns, wide=wide).fillna(0.0)
    cum = np.expm1(w.cumsum()) if log else (1.0 + w).cumprod() - 1.0
    return cum if wide else to_tidy(cum, "cumret")


def rebased_prices(
    prices: pd.DataFrame, *, base: float = 100.0, field: str = "adj_close", wide: bool = False
) -> pd.DataFrame:
    """Price index rebased to ``base`` at each series' first valid observation.

    ``base * p_t / p_0`` per ticker — the canonical multi-asset "performance overlay" (every line
    starts at ``base``, so co-movement / divergence / lead-lag are read directly). Equivalent to
    ``base * (1 + cumulative_returns)`` but anchored at the first price date, not the first return.
    """
    pw = _prices_wide(prices, field, wide)
    if pw.empty:
        return pw if wide else to_tidy(pw, "rebased")
    first = pw.bfill().iloc[0]
    rb = base * pw.div(first, axis=1)
    return rb if wide else to_tidy(rb, "rebased")


def resample_returns(
    returns: pd.DataFrame, freq: str = "ME", *, log: bool = False, wide: bool = False
) -> pd.DataFrame:
    """Aggregate higher-frequency returns to a lower frequency.

    log: sum within each bucket; simple: compound ``prod(1+r) - 1``. ``freq`` is a pandas offset
    alias (e.g. ``"ME"`` month-end, ``"W"`` weekly).
    """
    w = to_wide_values(returns, wide=wide)
    if log:
        agg = w.resample(freq).sum(min_count=1)
    else:
        agg = w.resample(freq).apply(lambda s: (1.0 + s).prod() - 1.0 if s.notna().any() else np.nan)
    return agg if wide else to_tidy(agg, "ret")
