"""Price & corporate actions (Panel 2)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Path, Query
from quant_core.data import DatasetMeta, adjustment_factor

from ..config import Settings, get_settings
from ..deps import get_catalog, load_ohlcv, resolve_dataset
from ..schemas.common import TICKER_PATTERN, SeriesMeta
from ..schemas.ohlcv import ActionMarker, CorporateActionsResponse, OHLCVBar, OHLCVResponse
from ..services.downsample import select_indices
from ..services.serialization import epoch_ms, jnum, series_points

router = APIRouter()


def _source_label(catalog, ticker, interval, source, settings) -> str | None:
    meta = resolve_dataset(catalog, ticker, interval=interval, source=source)
    if meta is not None:
        return meta.source
    return "synthetic" if settings.allow_synthetic else None


@router.get("/ohlcv/{ticker}", response_model=OHLCVResponse, operation_id="getOhlcv")
def get_ohlcv(
    ticker: str = Path(pattern=TICKER_PATTERN),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    interval: str = Query(default="1d"),
    source: str | None = Query(default=None),
    max_points: int | None = Query(default=None),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> OHLCVResponse:
    df = load_ohlcv(settings, catalog, ticker, start=start, end=end, interval=interval, source=source)
    label = _source_label(catalog, ticker, interval, source, settings)
    if df.empty:
        return OHLCVResponse(
            ticker=ticker, interval=interval, bars=[],
            meta=SeriesMeta(source=label, empty=True),
        )
    cap = max_points or settings.max_series_points
    keep = select_indices(df["close"].to_numpy(dtype=float), cap)
    bars = [
        OHLCVBar(
            t=epoch_ms(df["date"].iloc[i]),
            o=jnum(df["open"].iloc[i]),
            h=jnum(df["high"].iloc[i]),
            low=jnum(df["low"].iloc[i]),
            c=jnum(df["close"].iloc[i]),
            adj=jnum(df["adj_close"].iloc[i]),
            v=jnum(df["volume"].iloc[i]),
        )
        for i in keep
    ]
    return OHLCVResponse(
        ticker=ticker,
        interval=interval,
        bars=bars,
        meta=SeriesMeta(
            source=label,
            n_raw=int(len(df)),
            n_returned=len(bars),
            downsampled=len(bars) < len(df),
            start=df["date"].iloc[0].isoformat(),
            end=df["date"].iloc[-1].isoformat(),
        ),
    )


@router.get("/corporate-actions/{ticker}", response_model=CorporateActionsResponse, operation_id="getCorporateActions")
def get_corporate_actions(
    ticker: str = Path(pattern=TICKER_PATTERN),
    start: str | None = Query(default=None),
    end: str | None = Query(default=None),
    interval: str = Query(default="1d"),
    source: str | None = Query(default=None),
    settings: Settings = Depends(get_settings),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> CorporateActionsResponse:
    df = load_ohlcv(settings, catalog, ticker, start=start, end=end, interval=interval, source=source)
    label = _source_label(catalog, ticker, interval, source, settings)
    if df.empty:
        return CorporateActionsResponse(
            ticker=ticker, adj_factor=[], dividends=[], splits=[],
            meta=SeriesMeta(source=label, empty=True),
        )
    factor = adjustment_factor(df, ticker)
    pts, n_raw, n_ret, ds = series_points(factor.index, factor.to_numpy(), max_points=settings.max_series_points)

    divs = df[df["dividends"] > 0]
    dividends = [
        ActionMarker(t=epoch_ms(d), kind="dividend", value=float(v))
        for d, v in zip(divs["date"], divs["dividends"], strict=True)
    ]
    spl = df[(df["splits"] != 0) & (df["splits"] != 1)]
    splits = [
        ActionMarker(t=epoch_ms(d), kind="split", value=float(v))
        for d, v in zip(spl["date"], spl["splits"], strict=True)
    ]

    return CorporateActionsResponse(
        ticker=ticker,
        adj_factor=pts,
        dividends=dividends,
        splits=splits,
        meta=SeriesMeta(source=label, n_raw=n_raw, n_returned=n_ret, downsampled=ds),
    )
