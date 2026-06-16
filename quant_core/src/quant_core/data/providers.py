"""Market-data providers.

A :class:`Provider` knows how to ``fetch`` raw OHLCV for a set of tickers and return
it in the canonical tidy schema (:mod:`quant_core.data.schema`). The default,
:class:`YFinanceProvider`, wraps yfinance; :class:`PolygonProvider` is a stub wired
for later (Polygon → Databento → tick data, per the roadmap).

Provider contract::

    fetch(tickers, start, end, interval="1d") -> canonical tidy DataFrame

The normalization that turns yfinance's quirky output (single- vs multi-ticker column
shapes, the ``auto_adjust`` default that drops ``Adj Close``) into the canonical schema
lives here and is unit-tested against a raw-yfinance-shaped fixture.
"""

from __future__ import annotations

import os
from typing import Protocol, runtime_checkable

import pandas as pd

from . import schema

# yfinance field name -> canonical column name.
_YF_FIELD_MAP: dict[str, str] = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
    "Dividends": "dividends",
    "Stock Splits": "splits",
}


@runtime_checkable
class Provider(Protocol):
    """A market-data source that returns canonical tidy OHLCV."""

    name: str

    def fetch(
        self,
        tickers: list[str],
        start: str,
        end: str,
        interval: str = "1d",
    ) -> pd.DataFrame:  # pragma: no cover - protocol signature
        ...


def normalize_yfinance(raw: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    """Turn a raw ``yf.download(..., auto_adjust=False, actions=True)`` frame into canonical tidy.

    Handles both column shapes yfinance produces:
    - single ticker  -> flat columns (Open, High, ... Adj Close, ...)
    - many tickers    -> MultiIndex columns (ticker, field) when ``group_by="ticker"``

    Raises if ``Adj Close`` is absent — that means ``auto_adjust`` was effectively True
    and the raw-vs-adjusted distinction (the whole point of Project 1) would silently
    collapse, so we fail loudly instead of returning misleading data.
    """
    if raw is None or len(raw) == 0:
        return schema.empty_frame()

    if not _has_adj_close(raw):
        raise ValueError(
            "No 'Adj Close' column in the yfinance response — it likely returned "
            "auto-adjusted prices (auto_adjust=True). Fetch with auto_adjust=False so "
            "raw Close and Adj Close are both available (Project 1's whole point)."
        )

    blocks: list[pd.DataFrame] = []

    if isinstance(raw.columns, pd.MultiIndex):
        # Figure out which column level holds the tickers (group_by="ticker" => level 0).
        lvl0 = set(map(str, raw.columns.get_level_values(0)))
        ticker_level = 0 if lvl0 & set(tickers) else 1
        present = list(dict.fromkeys(raw.columns.get_level_values(ticker_level)))
        for tk in present:
            sub = raw.xs(tk, axis=1, level=ticker_level)
            blocks.append(_block_from_fields(sub, str(tk)))
    else:
        # Flat columns => exactly one ticker.
        tk = tickers[0] if tickers else "UNKNOWN"
        blocks.append(_block_from_fields(raw, tk))

    tidy = pd.concat(blocks, ignore_index=True) if blocks else schema.empty_frame()
    tidy = schema.ensure_schema(tidy)

    if not tidy.empty and tidy["adj_close"].isna().all():
        raise ValueError(
            "No 'Adj Close' data after normalization — yfinance likely returned "
            "auto-adjusted prices. Fetch with auto_adjust=False so raw Close and "
            "Adj Close are both available."
        )
    return tidy


def _has_adj_close(raw: pd.DataFrame) -> bool:
    """True if a raw yfinance frame carries an 'Adj Close' field in any column level."""
    if isinstance(raw.columns, pd.MultiIndex):
        for level in range(raw.columns.nlevels):
            if "Adj Close" in set(raw.columns.get_level_values(level)):
                return True
        return False
    return "Adj Close" in raw.columns


def _block_from_fields(fields_df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Build a canonical (pre-schema) block for one ticker from a fields-only frame."""
    block = fields_df.rename(columns=_YF_FIELD_MAP).copy()
    block = block.reset_index()
    # yfinance names the index 'Date' (daily) or 'Datetime' (intraday).
    index_col = block.columns[0]
    block = block.rename(columns={index_col: "date"})
    block["ticker"] = ticker
    for col in ("dividends", "splits"):
        if col not in block.columns:
            block[col] = 0.0
    keep = [c for c in schema.OHLCV_COLUMNS if c in block.columns]
    return block[keep]


class YFinanceProvider:
    """Default provider — wraps yfinance. Needs the ``quant-core[yfinance]`` extra."""

    name = "yfinance"

    def fetch(
        self,
        tickers: list[str],
        start: str,
        end: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        try:
            import yfinance as yf
        except ModuleNotFoundError as exc:  # pragma: no cover - import guard
            raise ModuleNotFoundError(
                "yfinance is required for YFinanceProvider. "
                "Install the extra: `uv add 'quant-core[yfinance]'`."
            ) from exc

        raw = yf.download(
            tickers=tickers,
            start=start,
            end=end,
            interval=interval,
            auto_adjust=False,   # CRITICAL: keep raw Close AND a separate Adj Close column
            actions=True,        # attach Dividends and Stock Splits columns
            group_by="ticker",
            progress=False,
            threads=True,
        )
        return normalize_yfinance(raw, list(tickers))


class PolygonProvider:
    """Stub for Polygon.io (roadmap project 1 mentions yfinance/Polygon).

    Wired for later: reads ``POLYGON_API_KEY`` from the environment (load a ``.env``
    with python-dotenv before constructing). ``fetch`` is not implemented yet.
    """

    name = "polygon"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("POLYGON_API_KEY")

    def fetch(
        self,
        tickers: list[str],
        start: str,
        end: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        raise NotImplementedError(
            "PolygonProvider is a stub. Add the `quant-core[polygon]` extra and "
            "implement fetch() when you reach the Polygon/Databento phase."
        )
