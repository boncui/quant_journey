"""Catalog, coverage, and refresh (Panel 1)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from quant_core.data import DatasetMeta
from quant_core.data import coverage as qc_coverage

from ..config import Settings, get_settings
from ..deps import get_catalog, resolve_dataset
from ..schemas.catalog import (
    CatalogResponse,
    CoverageOut,
    DatasetMetaOut,
    RefreshRequest,
    RefreshResponse,
)
from ..schemas.common import TICKER_PATTERN

router = APIRouter()


def _iso(ts) -> str | None:
    return ts.isoformat() if ts is not None else None


def _to_out(m: DatasetMeta) -> DatasetMetaOut:
    return DatasetMetaOut(
        source=m.source,
        tickers=m.tickers,
        interval=m.interval,
        n_rows=m.n_rows,
        n_bytes=m.n_bytes,
        start=_iso(m.start),
        end=_iso(m.end),
        modified_at=m.modified_at.isoformat(),
        provider=m.provider,
        fetched_at=m.fetched_at.isoformat() if m.fetched_at else None,
    )


@router.get("/catalog", response_model=CatalogResponse, operation_id="getCatalog")
def get_catalog_route(
    source: str | None = Query(default=None),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> CatalogResponse:
    metas = [m for m in catalog if source is None or m.source == source]
    items = [_to_out(m) for m in metas]
    universe = sorted({t for m in metas for t in m.tickers})
    empty = len(items) == 0
    return CatalogResponse(
        items=items,
        count=len(items),
        universe=universe,
        empty=empty,
        hint="No datasets found — run `make cc-seed` to generate synthetic data." if empty else None,
    )


@router.get("/catalog/{ticker}/coverage", response_model=list[CoverageOut], operation_id="getCoverage")
def get_coverage_route(
    ticker: str = Path(pattern=TICKER_PATTERN),
    interval: str = Query(default="1d"),
    calendar: str = Query(default="NYSE"),
    catalog: list[DatasetMeta] = Depends(get_catalog),
) -> list[CoverageOut]:
    meta = resolve_dataset(catalog, ticker, interval=interval)
    if meta is None:
        raise HTTPException(status_code=404, detail=f"No dataset for ticker {ticker!r}.")
    return [
        CoverageOut(
            ticker=r.ticker,
            interval=r.interval,
            start=_iso(r.start),
            end=_iso(r.end),
            n_present=r.n_present,
            n_expected=r.n_expected,
            missing_pct=round(r.missing_pct, 4),
            last_session_gap=r.last_session_gap,
        )
        for r in qc_coverage(meta, calendar=calendar)
    ]


@router.post("/refresh", response_model=RefreshResponse, operation_id="refresh")
def refresh_route(
    body: RefreshRequest | None = None,
    settings: Settings = Depends(get_settings),
) -> RefreshResponse:
    """Best-effort LOCAL fetch into the cache via quant_core (never used in CI; yfinance is best-effort)."""
    tickers = (body.tickers if body and body.tickers else settings.default_universe)
    try:
        from quant_core.data import download_ohlcv

        df = download_ohlcv(tickers, settings.default_start, settings.default_end)
        return RefreshResponse(ok=True, tickers=tickers, rows=int(len(df)), message="cache refreshed")
    except Exception as exc:  # network/yfinance failure is expected sometimes — report, don't crash
        return RefreshResponse(ok=False, tickers=tickers, rows=0, message=str(exc))
