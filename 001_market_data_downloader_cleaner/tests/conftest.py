"""Offline fixtures for Project 1 — a fake provider so the app runs without any network."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quant_core.data import schema

# Real consecutive NYSE sessions (no holidays) so calendar-aware cleaning reports no gaps.
SESSIONS = [
    "2021-06-01", "2021-06-02", "2021-06-03", "2021-06-04",
    "2021-06-07", "2021-06-08", "2021-06-09", "2021-06-10",
]


def make_tidy(ticker, dates, *, close_base=100.0, dividends=None, splits=None, adj_close=None):
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
    name = "fake"

    def __init__(self, frames: dict[str, pd.DataFrame]):
        self._frames = frames
        self.calls: list = []

    def fetch(self, tickers, start, end, interval="1d") -> pd.DataFrame:
        self.calls.append((tuple(tickers), start, end, interval, "auto_adjust=False"))
        blocks = [self._frames[t] for t in tickers if t in self._frames]
        if not blocks:
            return schema.empty_frame()
        return schema.ensure_schema(pd.concat(blocks, ignore_index=True))


@pytest.fixture
def dividend_payer() -> pd.DataFrame:
    # adj_close below close before the 06-04 ex-dividend date -> raw vs adjusted diverges.
    n = len(SESSIONS)
    close = 100.0 + np.arange(n, dtype=float)
    adj = close.copy()
    ex = SESSIONS.index("2021-06-04")
    adj[:ex] -= 1.0  # back-adjustment before the dividend
    return make_tidy("KO", SESSIONS, dividends={"2021-06-04": 1.0}, adj_close=adj)


@pytest.fixture
def split_only() -> pd.DataFrame:
    # No dividends -> adj_close == close -> a split alone does not diverge.
    return make_tidy("AAPL", SESSIONS, splits={"2021-06-04": 4.0})


@pytest.fixture
def provider(dividend_payer, split_only) -> FakeProvider:
    return FakeProvider({"KO": dividend_payer, "AAPL": split_only})
