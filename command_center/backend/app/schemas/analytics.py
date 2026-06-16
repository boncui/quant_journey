"""Analytics schemas: returns/distribution (Panel 4), rolling (5), performance overlay (3),
correlation (6), and beta."""

from __future__ import annotations

from pydantic import BaseModel

from .common import NamedSeries, Point, SeriesMeta


class ReturnsResponse(BaseModel):
    ticker: str
    kind: str
    series: list[Point]
    meta: SeriesMeta


class HistogramOut(BaseModel):
    counts: list[float]
    bin_edges: list[float]
    bin_centers: list[float]
    density: bool


class MomentsOut(BaseModel):
    n: int
    mean: float | None
    std: float | None
    skew: float | None
    kurtosis_excess: float | None


class NormalOut(BaseModel):
    mu: float
    sigma: float
    jb_stat: float
    jb_pvalue: float


class QQOut(BaseModel):
    theoretical: list[float]
    sample: list[float]
    slope: float
    intercept: float


class DistributionResponse(BaseModel):
    ticker: str
    kind: str
    histogram: HistogramOut
    moments: MomentsOut
    normal: NormalOut | None = None     # null when scipy ([stats] extra) is unavailable
    qq: QQOut | None = None
    drawdown: list[Point]
    meta: SeriesMeta


class RollingResponse(BaseModel):
    ticker: str
    stat: str
    window: int
    annualized: bool
    series: list[Point]
    meta: SeriesMeta


class PerformanceResponse(BaseModel):
    tickers: list[str]
    base: float
    series: list[NamedSeries]           # per-ticker cumulative return rebased to `base`
    meta: SeriesMeta


class CorrelationResponse(BaseModel):
    tickers: list[str]                  # in cluster order when clustering applied
    matrix: list[list[float | None]]    # null cells = undefined (insufficient overlap)
    method: str
    clustered: bool
    meta: SeriesMeta


class BetaResponse(BaseModel):
    ticker: str
    benchmark: str
    beta: float | None
    alpha: float | None
    r_squared: float | None
    n: int
    rolling: list[Point] | None = None
    meta: SeriesMeta
