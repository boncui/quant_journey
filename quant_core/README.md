# quant_core

The shared mini-library for the [100-project quant journey](../README.md). Reusable logic
graduates into this package; each `NNN_*` project folder is a thin runnable app + report on
top of it. This is the "compounding" asset the roadmap is built around.

## Install / use

`quant_core` is consumed by each project as an **editable path dependency** with a pinned
version range, so projects always build against local source but break loudly if the API
moves out from under them:

```toml
# in a project's pyproject.toml
[project]
dependencies = ["quant-core[yfinance]>=0.1,<0.2"]

[tool.uv.sources]
quant-core = { path = "../quant_core", editable = true }
```

Base deps are lean and universal (`pandas`, `numpy`, `pyarrow`, `pandas-market-calendars`,
`python-dotenv`). Heavier stacks are **opt-in extras** so projects install only what they need:

| extra | pulls | used from |
|-------|-------|-----------|
| `yfinance` | yfinance | Phase 1 (data) |
| `polygon`  | polygon-api-client | later data phases |
| `econ`     | statsmodels, arch | Phase 4 |
| `opt`      | cvxpy | Phase 3 |
| `ml`       | scikit-learn | Phase 8 |

## API-evolution policy (semver)

- **Within a minor** (`0.1.x`): additive only — never rename or remove public API.
- **Breaking changes bump the minor** (`0.1` → `0.2`). Projects opt in by widening their pin.
- When `quant_core` dependencies change, every project must re-lock
  (`uv lock --upgrade-package quant-core`) and re-commit its `uv.lock`. `make relock-all` does this.

## Canonical data schema

There is ONE in-memory representation for OHLCV: a **tidy-long** `DataFrame`, one row per
(date, ticker):

| column | dtype | notes |
|--------|-------|-------|
| `date` | `datetime64[ns, UTC]` | tz-aware; daily bars at UTC midnight |
| `ticker` | `category` | symbol |
| `open`/`high`/`low`/`close` | `float64` | `close` is **raw** (already split-adjusted by yfinance) |
| `adj_close` | `float64` | additionally **dividend** back-adjusted |
| `volume` | `float64` | float so missing sessions can be NaN |
| `dividends` | `float64` | cash dividend on the ex-date, else 0.0 |
| `splits` | `float64` | split ratio on the split date, else 0.0/1.0 |

Wide matrices (date index × ticker columns) are derived on demand with
`to_wide(df, field="adj_close")` / `from_wide(...)`.

## Public API

```python
from quant_core.data import (
    download_ohlcv,          # provider + cache orchestration -> canonical tidy frame
    clean_ohlcv, CleanReport, # exchange-calendar-aware gap detection + validation
    to_wide, from_wide, ensure_schema, empty_frame, OHLCV_COLUMNS,
    Provider, YFinanceProvider, PolygonProvider, normalize_yfinance,
    adjustment_factor, ex_dividend_dates, split_dates, divergence,
)
```

Subpackages `backtest`, `metrics`, `portfolio`, `factors`, `stats` are stubs, filled in as the
roadmap reaches their phases.

## Develop & test

```bash
cd quant_core
uv sync                 # builds the editable install + dev deps
uv run pytest           # offline unit tests (no network)
uv run ruff check ..    # lint repo-wide
```
