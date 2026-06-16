"""quant_core.data — the reusable market-data layer.

Public API (stable within the 0.1.x minor; additive-only):
    download_ohlcv, clean_ohlcv, CleanReport
    to_wide, from_wide, ensure_schema, empty_frame, OHLCV_COLUMNS
    Provider, YFinanceProvider, PolygonProvider, normalize_yfinance
    adjustment_factor, ex_dividend_dates, split_dates, divergence
    make_synthetic_ohlcv
    DatasetMeta, CoverageReport, build_catalog, scan_parquet, discover_roots, coverage
"""

from __future__ import annotations

from .catalog import (
    CoverageReport,
    DatasetMeta,
    build_catalog,
    coverage,
    discover_roots,
    scan_parquet,
)
from .clean import CleanReport, TickerReport, clean_ohlcv, expected_sessions
from .corporate_actions import (
    adjustment_factor,
    divergence,
    ex_dividend_dates,
    split_dates,
)
from .loader import download_ohlcv
from .providers import (
    PolygonProvider,
    Provider,
    YFinanceProvider,
    normalize_yfinance,
)
from .schema import OHLCV_COLUMNS, empty_frame, ensure_schema, from_wide, to_wide
from .synthetic import make_synthetic_ohlcv

__all__ = [
    "download_ohlcv",
    "clean_ohlcv",
    "expected_sessions",
    "CleanReport",
    "TickerReport",
    "to_wide",
    "from_wide",
    "ensure_schema",
    "empty_frame",
    "OHLCV_COLUMNS",
    "Provider",
    "YFinanceProvider",
    "PolygonProvider",
    "normalize_yfinance",
    "adjustment_factor",
    "ex_dividend_dates",
    "split_dates",
    "divergence",
    "make_synthetic_ohlcv",
    "DatasetMeta",
    "CoverageReport",
    "build_catalog",
    "scan_parquet",
    "discover_roots",
    "coverage",
]
