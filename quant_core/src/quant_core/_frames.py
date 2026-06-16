"""Internal tidy<->wide helpers for derived frames (returns, rolling stats, ...).

``schema.to_wide`` pivots canonical OHLCV (its ``field`` must be an OHLCV column). Derived
analytics produce frames like ``[date, ticker, <value>]`` whose value column is not an OHLCV
field, so they use these helpers instead. Not part of the public API.
"""

from __future__ import annotations

import pandas as pd


def to_wide_values(frame: pd.DataFrame, *, wide: bool = False, value: str | None = None) -> pd.DataFrame:
    """Tidy ``[date, ticker, <value>]`` -> wide (date index x ticker columns). Pass-through if wide."""
    if wide:
        return frame
    cols = [c for c in frame.columns if c not in ("date", "ticker")]
    if not cols:
        raise ValueError("Expected a value column besides date/ticker.")
    val = value or cols[0]
    w = frame.pivot_table(index="date", columns="ticker", values=val, observed=True)
    w.columns.name = "ticker"
    return w.sort_index()


def to_tidy(wide: pd.DataFrame, value_name: str) -> pd.DataFrame:
    """Wide (date index x ticker columns) -> tidy ``[date, ticker, value_name]``, dropping NaN."""
    if wide.empty:
        return pd.DataFrame(
            {"date": pd.Series(dtype="datetime64[ns, UTC]"), "ticker": [], value_name: []}
        )
    long = (
        wide.reset_index()
        .melt(id_vars="date", var_name="ticker", value_name=value_name)
        .dropna(subset=[value_name])
        .sort_values(["ticker", "date"])
        .reset_index(drop=True)
    )
    long["ticker"] = long["ticker"].astype("category")
    return long
