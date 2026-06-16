"""Deterministic synthetic OHLCV — so the terminal (and tests) work offline with no prior fetch.

Market data parquet is gitignored and yfinance data can't be redistributed, so a fresh clone
has *no* data. This generator produces canonical tidy-long OHLCV with **zero network**, used as
``command_center``'s default seed and as offline test fixtures.

It also plants a known structure: every ticker loads on a shared **market factor** with a
per-ticker beta plus idiosyncratic noise, so the realized cross-ticker correlation is *known by
construction*. That makes the correlation / performance panels self-checking — you can verify the
app surfaces a pattern you deliberately put there.

Everything is seeded (``numpy.random.default_rng(seed)``) → identical output every run.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import schema
from .clean import expected_sessions


def make_synthetic_ohlcv(
    tickers: list[str] | None = None,
    start: str = "2018-01-01",
    end: str = "2024-01-01",
    *,
    interval: str = "1d",
    calendar: str = "NYSE",
    seed: int = 7,
    market_vol: float = 0.01,
    market_drift: float = 0.0003,
    betas: dict[str, float] | None = None,
    idio_vol: float = 0.008,
    annual_dividend_yield: float = 0.02,
    base_price: float = 100.0,
) -> pd.DataFrame:
    """Generate canonical tidy-long OHLCV for ``tickers`` over ``[start, end]``.

    Prices follow ``r_i,t = drift + beta_i * market_t + idio_i,t`` (a one-factor model), so the
    induced correlation between two tickers is determined by their betas and ``idio_vol`` — a
    ground-truth pattern. Raw ``close`` is the price path (already "split-adjusted" in spirit);
    ``adj_close`` is dividend-back-adjusted, so ``adj_close/close`` steps down going back across
    ex-dividend dates exactly like real adjusted series (Project 1's lesson).
    """
    if tickers is None:
        tickers = ["SPY", "KO", "AAPL"]
    rng = np.random.default_rng(seed)

    sessions = expected_sessions(start, end, calendar=calendar)
    n = len(sessions)
    if n == 0:
        return schema.empty_frame()

    # Shared market factor (the planted common driver).
    market = rng.normal(market_drift, market_vol, size=n)

    if betas is None:
        # Deterministic, spread-out betas so correlations differ across the universe.
        betas = {tk: 0.6 + 0.25 * i for i, tk in enumerate(tickers)}

    blocks: list[pd.DataFrame] = []
    for tk in tickers:
        beta = float(betas.get(tk, 1.0))
        idio = rng.normal(0.0, idio_vol, size=n)
        rets = beta * market + idio
        close = base_price * np.exp(np.cumsum(rets))

        # Intrabar OHLC consistent with the schema's sanity checks (high>=max(open,close), etc.).
        daily_range = np.abs(rng.normal(0.0, idio_vol, size=n)) * close
        prev_close = np.concatenate([[close[0]], close[:-1]])
        open_ = prev_close * (1.0 + rng.normal(0.0, idio_vol / 2, size=n))
        high = np.maximum(open_, close) + daily_range / 2
        low = np.minimum(open_, close) - daily_range / 2
        low = np.clip(low, 1e-6, None)
        volume = rng.uniform(5e5, 5e6, size=n).round()

        # Quarterly dividends (~every 63 trading sessions); cash amount from the annual yield.
        dividends = np.zeros(n)
        per_div = annual_dividend_yield / 4.0
        if annual_dividend_yield > 0:
            for ex in range(63, n, 63):
                dividends[ex] = round(close[ex] * per_div, 4)

        # Dividend back-adjustment: walk backwards, multiplying by (1 - div/close) at each ex-date.
        factor = np.ones(n)
        run = 1.0
        for t in range(n - 1, -1, -1):
            factor[t] = run
            if dividends[t] > 0 and close[t] > 0:
                run *= 1.0 - dividends[t] / close[t]
        adj_close = close * factor

        block = pd.DataFrame(
            {
                "date": sessions,
                "ticker": tk,
                "open": open_,
                "high": high,
                "low": low,
                "close": close,
                "adj_close": adj_close,
                "volume": volume,
                "dividends": dividends,
                "splits": np.zeros(n),
            }
        )
        blocks.append(block)

    return schema.ensure_schema(pd.concat(blocks, ignore_index=True))
