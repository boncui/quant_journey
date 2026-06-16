# Project 1 — Market data downloader & cleaner

> Roadmap #1 (Phase 1 · Foundations). *Pull OHLCV from yfinance for a universe of tickers;
> handle missing data, splits, and dividend adjustments.*
> **Learn:** data ingestion, corporate actions, and why "adjusted close" matters.

## What it does

1. **Download** OHLCV for a universe of tickers via `quant_core.data.download_ohlcv`
   (yfinance, `auto_adjust=False` so both raw `Close` and `Adj Close` are kept).
2. **Clean** against a real exchange calendar (`quant_core.data.clean_ohlcv`) — holidays are
   *not* mistaken for gaps; basic OHLC sanity is validated.
3. **Cache** the full history per ticker (parquet, TTL-aware) and write the cleaned slice to `data/`.
4. **Chart** raw `Close` vs `Adj Close` per ticker to `reports/`, annotating ex-dividend dates
   (green) and splits (red dashed).

### The actual lesson

Raw `Close` from yfinance is **already split-adjusted**, so a split does **not** make raw and
adjusted close diverge. The divergence you see comes from **dividend** back-adjustment — pick a
dividend payer (KO, SPY) over several years to see it clearly, and note that AAPL's 4:1 split on
2020-08-31 does *not* cause a jump between the two lines. The bottom panel plots
`adj_factor = adj_close / close`, which steps down at each ex-dividend date.

## Run

```bash
cd 001_market_data_downloader_cleaner
uv sync                       # builds editable quant_core[yfinance] + matplotlib
uv run python main.py --tickers SPY KO AAPL --start 2018-01-01 --end 2024-01-01
```

Useful flags: `--interval 1d`, `--calendar NYSE`, `--out data`, `--reports reports`, `--no-cache`.

## Test (offline)

```bash
uv run pytest                 # uses a fake provider — no network
```

## Reuse boundary

This app imports **only** `quant_core` + PyPI — never another project. The reusable download /
clean / corporate-actions logic lives in `quant_core.data`; this folder is just the runnable
app + report on top.

## ⚠️ Data / yfinance note

yfinance is an **unofficial** scraper of Yahoo Finance; its Terms of Service prohibit
redistribution and it breaks on upstream changes (so a live run is best-effort, non-deterministic).
Downloaded data (`data/`) and charts (`reports/`) are **gitignored and never committed**. Any
committed sample artifact must be generated from synthetic data, not Yahoo data.
