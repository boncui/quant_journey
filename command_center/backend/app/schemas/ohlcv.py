"""Price & corporate-actions schemas (Panel 2)."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Point, SeriesMeta


class OHLCVBar(BaseModel):
    t: int                 # epoch ms UTC
    o: float | None
    h: float | None
    low: float | None      # 'low' not 'l' — avoids the ambiguous single-letter identifier
    c: float | None        # raw close (split-adjusted)
    adj: float | None      # dividend-adjusted close
    v: float | None        # volume


class OHLCVResponse(BaseModel):
    ticker: str
    interval: str
    bars: list[OHLCVBar]
    meta: SeriesMeta


class ActionMarker(BaseModel):
    t: int
    kind: str              # "dividend" | "split"
    value: float           # cash dividend amount, or split ratio


class CorporateActionsResponse(BaseModel):
    ticker: str
    adj_factor: list[Point]
    dividends: list[ActionMarker]
    splits: list[ActionMarker]
    meta: SeriesMeta
