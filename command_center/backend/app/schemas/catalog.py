"""Catalog & coverage schemas (Panel 1)."""

from __future__ import annotations

from pydantic import BaseModel


class DatasetMetaOut(BaseModel):
    source: str
    tickers: list[str]
    interval: str | None
    n_rows: int
    n_bytes: int
    start: str | None
    end: str | None
    modified_at: str
    provider: str | None = None
    fetched_at: str | None = None


class CatalogResponse(BaseModel):
    items: list[DatasetMetaOut]
    count: int
    universe: list[str]           # distinct tickers across all datasets
    empty: bool
    hint: str | None = None       # shown by the catalog panel when empty


class CoverageOut(BaseModel):
    ticker: str
    interval: str
    start: str | None
    end: str | None
    n_present: int
    n_expected: int
    missing_pct: float
    last_session_gap: int


class RefreshRequest(BaseModel):
    tickers: list[str] | None = None


class RefreshResponse(BaseModel):
    ok: bool
    tickers: list[str]
    rows: int
    message: str
