"""Project 1 — Market data downloader & cleaner.

Pull OHLCV for a universe of tickers, clean it against a real exchange calendar, cache it,
and produce the deliverable: a `raw Close vs Adj Close` chart per ticker that shows *why
adjusted close matters*. The reusable data logic lives in `quant_core.data`; this file is
the thin runnable app + report on top of it.

Run:
    uv run python main.py --tickers SPY KO AAPL --start 2018-01-01 --end 2024-01-01

The chart teaches the real lesson: raw Close is already split-adjusted, so divergence
between raw and adjusted comes from **dividends** (pick a dividend payer like KO/SPY to see
it). A split (e.g. AAPL's 2020-08-31 4:1) does NOT cause divergence.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from quant_core.data import (
    Provider,
    adjustment_factor,
    clean_ohlcv,
    divergence,
    download_ohlcv,
    ex_dividend_dates,
    split_dates,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="001_market_data_downloader_cleaner",
        description="Download, clean, and chart OHLCV (raw vs adjusted close).",
    )
    p.add_argument("--tickers", nargs="+", default=["SPY", "KO", "AAPL"], help="ticker symbols")
    p.add_argument("--start", default="2018-01-01", help="start date YYYY-MM-DD")
    p.add_argument("--end", default="2024-01-01", help="end date YYYY-MM-DD")
    p.add_argument("--interval", default="1d", help="bar interval (default 1d)")
    p.add_argument("--calendar", default="NYSE", help="exchange calendar for gap detection")
    p.add_argument("--out", default="data", help="output dir for cleaned parquet")
    p.add_argument("--reports", default="reports", help="output dir for charts")
    p.add_argument("--no-cache", action="store_true", help="force a fresh fetch")
    return p


def run(
    tickers: list[str],
    start: str,
    end: str,
    *,
    out_dir: str | Path = "data",
    reports_dir: str | Path = "reports",
    interval: str = "1d",
    calendar: str = "NYSE",
    use_cache: bool = True,
    provider: Provider | None = None,
) -> dict:
    """Download -> clean -> cache -> chart. Returns a summary dict. Provider is injectable for tests."""
    out_dir = Path(out_dir)
    reports_dir = Path(reports_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    raw = download_ohlcv(
        tickers, start, end, interval=interval, provider=provider, use_cache=use_cache
    )
    clean, report = clean_ohlcv(raw, calendar=calendar)

    summary: dict = {"tickers": {}, "n_tickers": 0, "start": start, "end": end}
    if clean.empty:
        print(f"No data returned for {tickers} over {start}..{end}.")
        return summary

    for ticker in clean["ticker"].cat.categories:
        block = clean[clean["ticker"] == ticker]
        if block.empty:
            continue
        # Persist cleaned data.
        block.to_parquet(out_dir / f"{ticker}_{interval}.parquet", index=False)
        # Chart.
        chart_path = reports_dir / f"adjusted_vs_raw_{ticker}.png"
        _plot_adjusted_vs_raw(clean, str(ticker), chart_path)

        rep = report.per_ticker.get(str(ticker))
        summary["tickers"][str(ticker)] = {
            "rows": int(len(block)),
            "first": str(block["date"].min().date()),
            "last": str(block["date"].max().date()),
            "missing_sessions": rep.n_missing if rep else 0,
            "validation_violations": rep.n_validation_violations if rep else 0,
            "n_dividends": len(ex_dividend_dates(clean, str(ticker))),
            "n_splits": len(split_dates(clean, str(ticker))),
            "chart": str(chart_path),
        }
    summary["n_tickers"] = len(summary["tickers"])
    _print_summary(summary)
    return summary


def _print_summary(summary: dict) -> None:
    print(f"\nDownloaded {summary['n_tickers']} ticker(s) over {summary['start']}..{summary['end']}")
    print(f"{'ticker':<8}{'rows':>7}{'first':>14}{'last':>14}{'gaps':>7}{'bad':>6}{'divs':>7}{'splits':>8}")
    for tk, s in summary["tickers"].items():
        print(
            f"{tk:<8}{s['rows']:>7}{s['first']:>14}{s['last']:>14}"
            f"{s['missing_sessions']:>7}{s['validation_violations']:>6}{s['n_dividends']:>7}{s['n_splits']:>8}"
        )
        print(f"         chart -> {s['chart']}")


def _plot_adjusted_vs_raw(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    """Plot raw Close vs Adj Close for one ticker, annotating ex-dividend and split dates."""
    import matplotlib

    matplotlib.use("Agg")  # headless: no display, safe in CI/tests
    import matplotlib.pyplot as plt

    div = divergence(df, ticker)
    factor = adjustment_factor(df, ticker)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), sharex=True, height_ratios=[3, 1])
    ax1.plot(div.index, div["close"], label="raw Close (split-adjusted)", lw=1.2)
    ax1.plot(div.index, div["adj_close"], label="Adj Close (+ dividend-adjusted)", lw=1.2)
    for d in ex_dividend_dates(df, ticker):
        ax1.axvline(d, color="green", alpha=0.25, lw=0.8)
    for d in split_dates(df, ticker):
        ax1.axvline(d, color="red", alpha=0.5, lw=1.2, ls="--")
    ax1.set_title(f"{ticker}: raw vs adjusted close (divergence comes from dividends, not splits)")
    ax1.set_ylabel("price")
    ax1.legend(loc="best", fontsize=8)
    ax1.grid(alpha=0.3)

    ax2.plot(factor.index, factor.to_numpy(), color="purple", lw=1.0)
    ax2.set_ylabel("adj_factor")
    ax2.set_xlabel("date")
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=110)
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(
        args.tickers,
        args.start,
        args.end,
        out_dir=args.out,
        reports_dir=args.reports,
        interval=args.interval,
        calendar=args.calendar,
        use_cache=not args.no_cache,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
