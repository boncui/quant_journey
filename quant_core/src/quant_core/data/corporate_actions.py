"""Corporate-actions analysis: why "adjusted close" matters (roadmap project 1's lesson).

The teachable insight, stated precisely:

- yfinance's raw ``close`` is **already split-adjusted** — a stock split does NOT make
  raw and adjusted close diverge.
- ``adj_close`` adds **dividend back-adjustment** on top — so the divergence between raw
  ``close`` and ``adj_close`` comes from **dividends**, accumulating backwards in time.
- Yahoo's adjusted series is proprietary; we don't reconstruct it from raw factors. We
  expose the *empirical* adjustment factor ``adj_factor = adj_close / close`` (which steps
  at ex-dividend dates) plus the ex-dividend and split dates, and let the project plot it.

Everything here returns DATA (Series/lists). Plotting lives in the project, not in core.
"""

from __future__ import annotations

import pandas as pd


def adjustment_factor(df: pd.DataFrame, ticker: str | None = None) -> pd.Series:
    """``adj_close / close`` indexed by date. Steps down going back across ex-dividends.

    If ``ticker`` is given, filter to it; otherwise the frame must hold a single ticker.
    """
    block = _single_ticker(df, ticker)
    factor = (block["adj_close"] / block["close"]).rename("adj_factor")
    factor.index = pd.DatetimeIndex(block["date"])
    return factor


def ex_dividend_dates(df: pd.DataFrame, ticker: str | None = None) -> list[pd.Timestamp]:
    """Dates with a cash dividend (``dividends > 0``)."""
    block = _single_ticker(df, ticker)
    return list(pd.DatetimeIndex(block.loc[block["dividends"] > 0, "date"]))


def split_dates(df: pd.DataFrame, ticker: str | None = None) -> list[pd.Timestamp]:
    """Dates with a stock split (``splits`` not in {0, 1})."""
    block = _single_ticker(df, ticker)
    s = block["splits"]
    return list(pd.DatetimeIndex(block.loc[(s != 0) & (s != 1), "date"]))


def divergence(df: pd.DataFrame, ticker: str | None = None) -> pd.DataFrame:
    """Tidy per-date frame for plotting raw vs adjusted: ``close``, ``adj_close``, ``adj_factor``.

    Indexed by date. The project plots this; core does not import matplotlib.
    """
    block = _single_ticker(df, ticker)
    out = block[["close", "adj_close"]].copy()
    out["adj_factor"] = block["adj_close"].to_numpy() / block["close"].to_numpy()
    out.index = pd.DatetimeIndex(block["date"])
    return out


def _single_ticker(df: pd.DataFrame, ticker: str | None) -> pd.DataFrame:
    if ticker is not None:
        block = df[df["ticker"] == ticker]
    else:
        uniq = df["ticker"].unique()
        if len(uniq) != 1:
            raise ValueError(
                f"Expected a single ticker; got {len(uniq)}. Pass ticker=... to select one."
            )
        block = df
    return block.sort_values("date").reset_index(drop=True)
