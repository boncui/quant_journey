"""Write deterministic synthetic OHLCV into the seed dir so the catalog & charts have data offline.

`make cc-seed` runs ``python -m app.seed``. One parquet per ticker (``{ticker}_{interval}.parquet``)
so it matches the per-ticker file convention the catalog already understands. Pure synthetic — never
fetches the network, never commits (the seed dir is gitignored).
"""

from __future__ import annotations

from pathlib import Path

from quant_core.data import make_synthetic_ohlcv

from .config import get_settings


def seed_synthetic(
    seed_dir: Path | None = None,
    tickers: list[str] | None = None,
    start: str | None = None,
    end: str | None = None,
    interval: str = "1d",
) -> list[Path]:
    """Generate one synthetic parquet per ticker. Returns the written paths."""
    s = get_settings()
    seed_dir = Path(seed_dir or s.seed_dir)
    tickers = tickers or s.default_universe
    start = start or s.default_start
    end = end or s.default_end
    seed_dir.mkdir(parents=True, exist_ok=True)

    df = make_synthetic_ohlcv(tickers, start, end, interval=interval)
    written: list[Path] = []
    for ticker in df["ticker"].cat.categories:
        block = df[df["ticker"] == ticker]
        if block.empty:
            continue
        path = seed_dir / f"{ticker}_{interval}.parquet"
        block.to_parquet(path, index=False)
        written.append(path)
    return written


def main() -> int:
    paths = seed_synthetic()
    print(f"Seeded {len(paths)} synthetic dataset(s):")
    for p in paths:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
