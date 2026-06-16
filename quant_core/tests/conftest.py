"""Shared offline fixtures: synthetic canonical frames + raw-yfinance-shaped frames.

Nothing here touches the network. The raw-yfinance-shaped builders mimic exactly what
``yf.download(..., auto_adjust=False, actions=True, group_by="ticker")`` returns so the
normalization path (the riskiest code) is exercised without yfinance installed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quant_core.data import schema

_YF_FIELDS = ["Open", "High", "Low", "Close", "Adj Close", "Volume", "Dividends", "Stock Splits"]


def _fields_frame(dates: pd.DatetimeIndex, *, base: float, adj_factor: float = 1.0) -> pd.DataFrame:
    """One ticker's fields-only frame in yfinance's raw layout (DatetimeIndex named 'Date')."""
    n = len(dates)
    close = base + np.arange(n, dtype=float)
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Adj Close": close * adj_factor,
            "Volume": np.full(n, 1_000_000.0),
            "Dividends": np.zeros(n),
            "Stock Splits": np.zeros(n),
        },
        index=pd.DatetimeIndex(dates, name="Date"),
    )
    return df


@pytest.fixture
def trading_dates() -> pd.DatetimeIndex:
    # Five consecutive NYSE sessions (no holidays in this window).
    return pd.DatetimeIndex(["2021-06-01", "2021-06-02", "2021-06-03", "2021-06-04", "2021-06-07"])


@pytest.fixture
def raw_yf_single(trading_dates) -> pd.DataFrame:
    """yfinance single-ticker shape: flat columns."""
    return _fields_frame(trading_dates, base=100.0)


@pytest.fixture
def raw_yf_multi(trading_dates) -> pd.DataFrame:
    """yfinance multi-ticker shape: MultiIndex columns (ticker, field), group_by='ticker'."""
    aapl = _fields_frame(trading_dates, base=100.0)
    msft = _fields_frame(trading_dates, base=200.0)
    raw = pd.concat({"AAPL": aapl, "MSFT": msft}, axis=1)
    raw.columns.names = ["Ticker", "Price"]
    return raw


@pytest.fixture
def raw_yf_no_adjclose(trading_dates) -> pd.DataFrame:
    """Simulate auto_adjust=True: Adj Close column is absent entirely."""
    return _fields_frame(trading_dates, base=100.0).drop(columns=["Adj Close"])


def make_tidy(
    ticker: str,
    dates,
    *,
    close_base: float = 100.0,
    dividends: dict[str, float] | None = None,
    splits: dict[str, float] | None = None,
    adj_close=None,
) -> pd.DataFrame:
    """Build a canonical tidy frame for one ticker (used to fake a Provider offline)."""
    dates = pd.DatetimeIndex(pd.to_datetime(list(dates)))
    n = len(dates)
    close = close_base + np.arange(n, dtype=float)
    div = np.zeros(n)
    spl = np.zeros(n)
    if dividends:
        for d, v in dividends.items():
            div[dates.get_loc(pd.Timestamp(d))] = v
    if splits:
        for d, v in splits.items():
            spl[dates.get_loc(pd.Timestamp(d))] = v
    frame = pd.DataFrame(
        {
            "date": dates,
            "ticker": ticker,
            "open": close - 0.5,
            "high": close + 1.0,
            "low": close - 1.0,
            "close": close,
            "adj_close": close if adj_close is None else np.asarray(adj_close, dtype=float),
            "volume": np.full(n, 1_000_000.0),
            "dividends": div,
            "splits": spl,
        }
    )
    return schema.ensure_schema(frame)


class FakeProvider:
    """A Provider that returns pre-built tidy frames — no network."""

    name = "fake"

    def __init__(self, frames: dict[str, pd.DataFrame]):
        self._frames = frames
        self.calls: list[tuple[tuple[str, ...], str, str, str]] = []

    def fetch(self, tickers, start, end, interval="1d") -> pd.DataFrame:
        self.calls.append((tuple(tickers), start, end, interval))
        blocks = [self._frames[t] for t in tickers if t in self._frames]
        if not blocks:
            return schema.empty_frame()
        return schema.ensure_schema(pd.concat(blocks, ignore_index=True))
