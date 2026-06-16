"""Cleaning & validation for canonical OHLCV.

The key correctness point (this is a data-quality teaching project): gaps are measured
against a **real exchange trading calendar**, not a naive business-day range. An exchange
holiday (Thanksgiving, July 4th) is *not* a missing bar, and we never forward-fill across
one by default — doing so would invent phantom prices that corrupt every downstream
return/vol calculation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from . import schema


@dataclass
class TickerReport:
    ticker: str
    n_expected_sessions: int
    n_present: int
    missing_sessions: list[pd.Timestamp] = field(default_factory=list)
    n_validation_violations: int = 0

    @property
    def n_missing(self) -> int:
        return len(self.missing_sessions)


@dataclass
class CleanReport:
    per_ticker: dict[str, TickerReport] = field(default_factory=dict)

    @property
    def total_missing(self) -> int:
        return sum(r.n_missing for r in self.per_ticker.values())

    @property
    def total_violations(self) -> int:
        return sum(r.n_validation_violations for r in self.per_ticker.values())


def expected_sessions(start, end, calendar: str = "NYSE") -> pd.DatetimeIndex:
    """Trading sessions for an exchange between ``start`` and ``end`` (tz-aware UTC, normalized)."""
    import pandas_market_calendars as mcal

    cal = mcal.get_calendar(calendar)
    days = cal.valid_days(start_date=pd.Timestamp(start).date(), end_date=pd.Timestamp(end).date())
    return pd.DatetimeIndex(days).tz_convert("UTC").normalize()


def clean_ohlcv(
    df: pd.DataFrame,
    *,
    calendar: str = "NYSE",
    fill: str = "none",
) -> tuple[pd.DataFrame, CleanReport]:
    """Validate and (optionally) gap-fill OHLCV against an exchange calendar.

    ``fill``:
        - ``"none"`` (default): do not invent rows; only report missing sessions.
        - ``"ffill"``: reindex each ticker to its expected sessions and forward-fill
          OHLC/adj_close (volume -> 0 on filled days). Use with care.

    Returns ``(clean_df, report)``. ``clean_df`` is always canonical-schema, sorted,
    de-duplicated; validation violations are reported, not dropped.
    """
    df = schema.ensure_schema(df)
    report = CleanReport()
    if df.empty:
        return df, report

    out_blocks: list[pd.DataFrame] = []
    for ticker, block in df.groupby("ticker", observed=True):
        block = block.sort_values("date")
        present = pd.DatetimeIndex(block["date"]).normalize()
        lo, hi = present.min(), present.max()
        sessions = expected_sessions(lo, hi, calendar=calendar)
        missing = sessions.difference(present)

        violations = _count_violations(block)
        report.per_ticker[str(ticker)] = TickerReport(
            ticker=str(ticker),
            n_expected_sessions=len(sessions),
            n_present=len(present),
            missing_sessions=list(missing),
            n_validation_violations=violations,
        )

        if fill == "ffill" and len(missing) > 0:
            block = _reindex_fill(block, str(ticker), sessions)
        out_blocks.append(block)

    clean = schema.ensure_schema(pd.concat(out_blocks, ignore_index=True))
    return clean, report


def _count_violations(block: pd.DataFrame) -> int:
    """Count rows breaking basic OHLC sanity (high>=low/open/close, low<=open/close, non-negative)."""
    b = block
    bad = (
        (b["high"] < b["low"])
        | (b["high"] < b["open"])
        | (b["high"] < b["close"])
        | (b["low"] > b["open"])
        | (b["low"] > b["close"])
        | (b[["open", "high", "low", "close"]] < 0).any(axis=1)
        | (b["volume"] < 0)
    )
    return int(bad.fillna(False).sum())


def _reindex_fill(block: pd.DataFrame, ticker: str, sessions: pd.DatetimeIndex) -> pd.DataFrame:
    indexed = block.set_index(pd.DatetimeIndex(block["date"]).normalize()).drop(columns=["date"])
    indexed = indexed[~indexed.index.duplicated(keep="last")].reindex(sessions)
    indexed["ticker"] = ticker
    for col in ("open", "high", "low", "close", "adj_close"):
        indexed[col] = indexed[col].ffill()
    indexed["volume"] = indexed["volume"].fillna(0.0)
    indexed[["dividends", "splits"]] = indexed[["dividends", "splits"]].fillna(0.0)
    indexed = indexed.reset_index(names="date")
    return indexed
