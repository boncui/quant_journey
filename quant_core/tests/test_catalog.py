"""Catalog discovery: project slices vs cache stay distinct; cheap metadata; coverage."""

from __future__ import annotations

from quant_core.data import build_catalog, coverage, make_synthetic_ohlcv, scan_parquet


def _write(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def test_catalog_discovers_project_and_cache_as_distinct_sources(tmp_path):
    proj = tmp_path / "001_demo" / "data"
    aapl = make_synthetic_ohlcv(["AAPL"], "2021-01-01", "2021-06-01", seed=1)
    _write(aapl, proj / "AAPL_1d.parquet")

    cache = tmp_path / "cache"
    ko = make_synthetic_ohlcv(["KO"], "2021-01-01", "2021-06-01", seed=2)
    _write(ko, cache / "KO_1d_deadbeef.parquet")

    catalog = build_catalog(tmp_path, cache_dir=cache)
    sources = {m.source for m in catalog}
    assert "project:001_demo" in sources
    assert "cache" in sources

    meta = next(m for m in catalog if "AAPL" in m.tickers)
    assert meta.n_rows == len(aapl)
    assert meta.interval == "1d"
    assert meta.start is not None and meta.end is not None
    assert meta.n_bytes > 0


def test_scan_parquet_date_span(tmp_path):
    spy = make_synthetic_ohlcv(["SPY"], "2020-01-01", "2020-06-01", seed=4)
    p = tmp_path / "SPY_1d.parquet"
    _write(spy, p)
    meta = scan_parquet(p, "cache")
    assert meta.tickers == ["SPY"]
    assert meta.start <= meta.end


def test_coverage_reports_per_ticker(tmp_path):
    aapl = make_synthetic_ohlcv(["AAPL"], "2021-01-01", "2021-06-01", seed=1)
    p = tmp_path / "001_x" / "data" / "AAPL_1d.parquet"
    _write(aapl, p)
    meta = scan_parquet(p, "project:001_x")
    cov = coverage(meta)
    assert len(cov) == 1
    assert cov[0].ticker == "AAPL"
    assert cov[0].n_present == meta.n_rows
    assert cov[0].missing_pct == 0.0   # synthetic data has no gaps vs the NYSE calendar
