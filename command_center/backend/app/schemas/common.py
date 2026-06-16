"""Shared schema primitives: enums, wire points, and the honest ``meta`` block."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

#: Ticker path-param guard (blocks path traversal; tickers resolve via the catalog, never a raw path).
TICKER_PATTERN = r"^[A-Z0-9.\-]{1,15}$"


class Interval(StrEnum):
    d1 = "1d"
    wk1 = "1wk"
    mo1 = "1mo"


class Field(StrEnum):
    open = "open"
    high = "high"
    low = "low"
    close = "close"
    adj_close = "adj_close"
    volume = "volume"


class ReturnKind(StrEnum):
    simple = "simple"
    log = "log"


class RollingStat(StrEnum):
    vol = "vol"
    mean = "mean"
    sharpe = "sharpe"


class Point(BaseModel):
    t: int                 # epoch milliseconds, UTC
    v: float | None        # null for gaps/NaN — rendered honestly, never interpolated


class NamedSeries(BaseModel):
    name: str
    points: list[Point]


class SeriesMeta(BaseModel):
    """Honest provenance/shape: where it came from, how big, whether it was downsampled."""

    source: str | None = None
    n_raw: int = 0
    n_returned: int = 0
    downsampled: bool = False
    start: str | None = None
    end: str | None = None
    empty: bool = False


class MetaOut(BaseModel):
    version: str
    quant_core_version: str
    api: str = "v1"
    sources: list[str] = []
