"""Canonical market-data schema for the whole quant journey.

There is ONE canonical in-memory representation for OHLCV data: a **tidy-long**
``DataFrame`` with one row per (date, ticker). Every provider normalizes into this
shape and every consumer (backtester, optimizer, factor models) reads it, so no
project re-invents column names or pivots.

Canonical columns (in order)::

    date       datetime64[ns, UTC]   tz-aware, UTC (daily bars sit at UTC midnight)
    ticker     category              the symbol
    open       float64
    high       float64
    low        float64
    close      float64               raw close (already split-adjusted by yfinance)
    adj_close  float64               additionally dividend-back-adjusted
    volume     float64               (float so missing sessions can be NaN)
    dividends  float64               cash dividend on the ex-date (0.0 otherwise)
    splits     float64               split ratio on the split date (0.0/1.0 otherwise)

Wide matrices (date index x ticker columns) are derived on demand via :func:`to_wide`.
"""

from __future__ import annotations

import pandas as pd

#: Canonical column order for the tidy-long OHLCV frame.
OHLCV_COLUMNS: list[str] = [
    "date",
    "ticker",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "dividends",
    "splits",
]

_FLOAT_COLUMNS: list[str] = [
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "dividends",
    "splits",
]


def empty_frame() -> pd.DataFrame:
    """Return an empty DataFrame with the canonical columns and dtypes."""
    df = pd.DataFrame({c: pd.Series(dtype="float64") for c in _FLOAT_COLUMNS})
    df.insert(0, "ticker", pd.Series(dtype="category"))
    df.insert(0, "date", pd.Series(dtype="datetime64[ns, UTC]"))
    return df[OHLCV_COLUMNS]


def ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce ``df`` to the canonical schema: columns, dtypes, tz, ordering.

    Missing optional columns (``dividends``/``splits``) are filled with ``0.0``.
    The ``date`` column is made tz-aware UTC (tz-naive input is localized to UTC,
    tz-aware input is converted). Rows are sorted by (ticker, date) and de-duplicated.
    """
    if df.empty:
        return empty_frame()

    out = df.copy()

    for col in ("dividends", "splits"):
        if col not in out.columns:
            out[col] = 0.0

    missing = [c for c in OHLCV_COLUMNS if c not in out.columns]
    if missing:
        raise ValueError(f"Frame is missing required columns: {missing}")

    # date -> tz-aware UTC at nanosecond resolution (stable across parquet round-trips)
    date = pd.to_datetime(out["date"])
    if getattr(date.dtype, "tz", None) is None:
        date = date.dt.tz_localize("UTC")
    else:
        date = date.dt.tz_convert("UTC")
    out["date"] = date.dt.as_unit("ns")

    out["ticker"] = out["ticker"].astype("category")
    for col in _FLOAT_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("float64")

    out = out[OHLCV_COLUMNS]
    out = (
        out.drop_duplicates(subset=["ticker", "date"])
        .sort_values(["ticker", "date"])
        .reset_index(drop=True)
    )
    return out


def to_wide(df: pd.DataFrame, field: str = "adj_close") -> pd.DataFrame:
    """Pivot tidy-long -> wide: a ``date`` index x ``ticker`` columns matrix of ``field``.

    This is what vectorized backtests (Phase 2) and portfolio optimizers (Phase 3) want.
    """
    if field not in OHLCV_COLUMNS or field in ("date", "ticker"):
        raise ValueError(f"field must be one of {_FLOAT_COLUMNS}, got {field!r}")
    if df.empty:
        return pd.DataFrame(index=pd.DatetimeIndex([], tz="UTC", name="date"))
    wide = df.pivot_table(index="date", columns="ticker", values=field, observed=True)
    wide.columns.name = "ticker"
    return wide.sort_index()


def from_wide(wide: pd.DataFrame, field: str = "adj_close") -> pd.DataFrame:
    """Inverse of :func:`to_wide` for a single field.

    Returns a tidy frame with ``date``, ``ticker`` and ``field`` columns (a partial
    reconstruction — other OHLCV fields are not present in a single wide matrix).
    """
    if wide.empty:
        return pd.DataFrame({"date": pd.Series(dtype="datetime64[ns, UTC]"), "ticker": [], field: []})
    long = (
        wide.reset_index()
        .melt(id_vars="date", var_name="ticker", value_name=field)
        .dropna(subset=[field])
        .sort_values(["ticker", "date"])
        .reset_index(drop=True)
    )
    long["ticker"] = long["ticker"].astype("category")
    return long
