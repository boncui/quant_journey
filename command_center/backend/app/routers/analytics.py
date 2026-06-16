"""Analytics endpoints — all thin wrappers over quant_core (no math here)."""

from __future__ import annotations

import pandas as pd
from fastapi import APIRouter, Depends, Path, Query
from quant_core.data import DatasetMeta
from quant_core.data.schema import ensure_schema
from quant_core.factors import capm_fit, rolling_beta
from quant_core.metrics import drawdown_series
from quant_core.portfolio import cluster_order, correlation_matrix
from quant_core.stats import (
    histogram,
    log_returns,
    moments,
    rebased_prices,
    rolling_mean,
    rolling_sharpe,
    rolling_vol,
    simple_returns,
)

from ..config import Settings, get_settings
from ..deps import get_catalog, load_ohlcv, resolve_dataset
from ..schemas.analytics import (
    BetaResponse,
    CorrelationResponse,
    DistributionResponse,
    HistogramOut,
    MomentsOut,
    NormalOut,
    PerformanceResponse,
    QQOut,
    ReturnsResponse,
    RollingResponse,
)
from ..schemas.common import (
    TICKER_PATTERN,
    Field,
    NamedSeries,
    Point,
    ReturnKind,
    RollingStat,
    SeriesMeta,
)
from ..services.serialization import epoch_ms, jnum, series_points, tidy_points

router = APIRouter()

_ROLLING = {
    RollingStat.vol: ("rolling_vol", lambda r, w, **k: rolling_vol(r, w, annualize=k["annualize"])),
    RollingStat.mean: ("rolling_mean", lambda r, w, **k: rolling_mean(r, w)),
    RollingStat.sharpe: ("rolling_sharpe", lambda r, w, **k: rolling_sharpe(r, w, rf=k["rf"])),
}


def _returns_tidy(df: pd.DataFrame, kind: ReturnKind, field: str) -> pd.DataFrame:
    fn = log_returns if kind == ReturnKind.log else simple_returns
    return fn(df, field=field)


def _source_label(catalog, ticker, settings, source=None) -> str | None:
    meta = resolve_dataset(catalog, ticker, source=source)
    if meta is not None:
        return meta.source
    return "synthetic" if settings.allow_synthetic else None


def _combined(settings, catalog, tickers, start, end, interval) -> pd.DataFrame:
    frames = [
        load_ohlcv(settings, catalog, t, start=start, end=end, interval=interval)
        for t in tickers
    ]
    frames = [f for f in frames if not f.empty]
    if not frames:
        return ensure_schema(pd.DataFrame())
    return ensure_schema(pd.concat(frames, ignore_index=True))


def _parse_tickers(tickers: str) -> list[str]:
    return [t.strip().upper() for t in tickers.split(",") if t.strip()]


@router.get("/returns/{ticker}", response_model=ReturnsResponse, operation_id="getReturns")
def get_returns(
    ticker: str = Path(pattern=TICKER_PATTERN),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    kind: ReturnKind = Query(default=ReturnKind.log),
    field: Field = Query(default=Field.adj_close),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> ReturnsResponse:
    df = load_ohlcv(settings, catalog, ticker, start=start, end=end)
    label = _source_label(catalog, ticker, settings)
    r = _returns_tidy(df, kind, field.value)
    pts, n_raw, n_ret, ds = tidy_points(r, "ret", max_points=settings.max_series_points)
    return ReturnsResponse(
        ticker=ticker, kind=kind.value, series=pts,
        meta=SeriesMeta(source=label, n_raw=n_raw, n_returned=n_ret, downsampled=ds, empty=r.empty),
    )


@router.get("/distribution/{ticker}", response_model=DistributionResponse, operation_id="getDistribution")
def get_distribution(
    ticker: str = Path(pattern=TICKER_PATTERN),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    kind: ReturnKind = Query(default=ReturnKind.log),
    field: Field = Query(default=Field.adj_close),
    bins: str = Query(default="fd"),
    qq: bool = Query(default=True),
    normality: bool = Query(default=True),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> DistributionResponse:
    df = load_ohlcv(settings, catalog, ticker, start=start, end=end)
    label = _source_label(catalog, ticker, settings)
    r = _returns_tidy(df, kind, field.value)
    rs = r.set_index("date")["ret"] if not r.empty else pd.Series(dtype=float)

    bins_arg: int | str = int(bins) if bins.isdigit() else bins
    h = histogram(rs, bins=bins_arg)
    m = moments(rs)
    normal_out = None
    qq_out = None
    if normality:
        try:
            from quant_core.stats import normality as _normality

            nf = _normality(rs)
            normal_out = NormalOut(mu=jnum(nf.mu), sigma=jnum(nf.sigma), jb_stat=jnum(nf.jb_stat), jb_pvalue=jnum(nf.jb_pvalue))
        except ModuleNotFoundError:
            normal_out = None
    if qq:
        try:
            from quant_core.stats import qq_points

            q = qq_points(rs)
            qq_out = QQOut(theoretical=q.theoretical, sample=q.sample, slope=jnum(q.slope), intercept=jnum(q.intercept))
        except ModuleNotFoundError:
            qq_out = None

    dd = drawdown_series(rs, is_returns=True)
    dd_pts, *_ = series_points(dd.index, dd.to_numpy(), max_points=settings.max_series_points) if len(dd) else ([], 0, 0, False)

    return DistributionResponse(
        ticker=ticker,
        kind=kind.value,
        histogram=HistogramOut(counts=h.counts, bin_edges=h.bin_edges, bin_centers=h.bin_centers, density=h.density),
        moments=MomentsOut(n=m.n, mean=jnum(m.mean), std=jnum(m.std), skew=jnum(m.skew), kurtosis_excess=jnum(m.kurtosis_excess)),
        normal=normal_out,
        qq=qq_out,
        drawdown=dd_pts,
        meta=SeriesMeta(source=label, n_raw=int(len(rs)), n_returned=int(len(rs)), empty=rs.empty),
    )


@router.get("/rolling/{ticker}", response_model=RollingResponse, operation_id="getRolling")
def get_rolling(
    ticker: str = Path(pattern=TICKER_PATTERN),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    window: int = Query(default=21, ge=2),
    stat: RollingStat = Query(default=RollingStat.vol),
    annualize: bool = Query(default=True),
    rf: float = Query(default=0.0),
    kind: ReturnKind = Query(default=ReturnKind.log),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> RollingResponse:
    df = load_ohlcv(settings, catalog, ticker, start=start, end=end)
    label = _source_label(catalog, ticker, settings)
    r = _returns_tidy(df, kind, Field.adj_close.value)
    col, fn = _ROLLING[stat]
    out = fn(r, window, annualize=annualize, rf=rf) if not r.empty else r.assign(**{col: []})
    pts, n_raw, n_ret, ds = tidy_points(out, col, max_points=settings.max_series_points) if not out.empty else ([], 0, 0, False)
    return RollingResponse(
        ticker=ticker, stat=stat.value, window=window, annualized=(annualize and stat != RollingStat.mean),
        series=pts,
        meta=SeriesMeta(source=label, n_raw=n_raw, n_returned=n_ret, downsampled=ds, empty=len(pts) == 0),
    )


@router.get("/performance", response_model=PerformanceResponse, operation_id="getPerformance")
def get_performance(
    tickers: str = Query(..., description="comma-separated tickers"),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    field: Field = Query(default=Field.adj_close),
    base: float = Query(default=100.0),
    interval: str = Query(default="1d"),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> PerformanceResponse:
    tlist = _parse_tickers(tickers)
    combined = _combined(settings, catalog, tlist, start, end, interval)
    if combined.empty:
        return PerformanceResponse(tickers=tlist, base=base, series=[], meta=SeriesMeta(empty=True))
    rb = rebased_prices(combined, base=base, field=field.value)
    series: list[NamedSeries] = []
    for t in tlist:
        sub = rb[rb["ticker"] == t].sort_values("date")
        if sub.empty:
            continue
        pts, *_ = series_points(sub["date"], sub["rebased"].to_numpy(), max_points=settings.max_series_points)
        series.append(NamedSeries(name=t, points=pts))
    return PerformanceResponse(
        tickers=tlist, base=base, series=series,
        meta=SeriesMeta(n_raw=int(len(combined)), n_returned=sum(len(s.points) for s in series), empty=not series),
    )


@router.get("/correlation", response_model=CorrelationResponse, operation_id="getCorrelation")
def get_correlation(
    tickers: str = Query(..., description="comma-separated tickers"),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    kind: ReturnKind = Query(default=ReturnKind.log),
    field: Field = Query(default=Field.adj_close),
    method: str = Query(default="pearson"),
    cluster: bool = Query(default=True),
    interval: str = Query(default="1d"),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> CorrelationResponse:
    tlist = _parse_tickers(tickers)
    combined = _combined(settings, catalog, tlist, start, end, interval)
    if combined.empty:
        return CorrelationResponse(tickers=tlist, matrix=[], method=method, clustered=False, meta=SeriesMeta(empty=True))
    r = _returns_tidy(combined, kind, field.value)
    corr = correlation_matrix(r, method=method)
    clustered = False
    if cluster and corr.shape[0] > 2:
        try:
            order = cluster_order(corr)
            corr = corr.loc[order, order]
            clustered = True
        except ModuleNotFoundError:
            clustered = False
    matrix = [[jnum(v) for v in row] for row in corr.to_numpy().tolist()]
    return CorrelationResponse(
        tickers=[str(c) for c in corr.columns],
        matrix=matrix,
        method=method,
        clustered=clustered,
        meta=SeriesMeta(n_raw=int(len(combined)), n_returned=corr.shape[0]),
    )


@router.get("/beta/{ticker}", response_model=BetaResponse, operation_id="getBeta")
def get_beta(
    ticker: str = Path(pattern=TICKER_PATTERN),
    benchmark: str = Query(default="SPY"),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    window: int | None = Query(default=None, ge=2),
    kind: ReturnKind = Query(default=ReturnKind.log),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> BetaResponse:
    a_df = load_ohlcv(settings, catalog, ticker, start=start, end=end)
    b_df = load_ohlcv(settings, catalog, benchmark, start=start, end=end)
    ar = _returns_tidy(a_df, kind, Field.adj_close.value)
    br = _returns_tidy(b_df, kind, Field.adj_close.value)
    a_s = ar.set_index("date")["ret"] if not ar.empty else pd.Series(dtype=float)
    b_s = br.set_index("date")["ret"] if not br.empty else pd.Series(dtype=float)
    fit = capm_fit(a_s, b_s)
    rolling_pts = None
    if window:
        rb = rolling_beta(a_s, b_s, window)
        rolling_pts = [Point(t=epoch_ms(d), v=jnum(v)) for d, v in rb.items()]
    return BetaResponse(
        ticker=ticker, benchmark=benchmark,
        beta=jnum(fit.beta), alpha=jnum(fit.alpha), r_squared=jnum(fit.r_squared), n=fit.n,
        rolling=rolling_pts,
        meta=SeriesMeta(n_raw=int(len(a_s)), n_returned=fit.n),
    )
