"""Offline tests for the Project 1 app. The data-layer correctness lives in quant_core's
tests; here we verify the app wiring: artifacts written, summary computed, graceful empties."""

from __future__ import annotations

from main import build_parser, run


def test_run_produces_parquet_and_charts(tmp_path, provider):
    out = tmp_path / "data"
    reports = tmp_path / "reports"
    summary = run(
        ["KO", "AAPL"],
        "2021-06-01",
        "2021-06-10",
        out_dir=out,
        reports_dir=reports,
        use_cache=False,
        provider=provider,
    )
    assert summary["n_tickers"] == 2
    for tk in ("KO", "AAPL"):
        assert (out / f"{tk}_1d.parquet").exists()
        assert (reports / f"adjusted_vs_raw_{tk}.png").exists()


def test_dividend_payer_has_dividends_split_only_has_splits(tmp_path, provider):
    summary = run(
        ["KO", "AAPL"],
        "2021-06-01",
        "2021-06-10",
        out_dir=tmp_path / "d",
        reports_dir=tmp_path / "r",
        use_cache=False,
        provider=provider,
    )
    assert summary["tickers"]["KO"]["n_dividends"] == 1
    assert summary["tickers"]["KO"]["n_splits"] == 0
    assert summary["tickers"]["AAPL"]["n_splits"] == 1
    assert summary["tickers"]["AAPL"]["n_dividends"] == 0


def test_no_calendar_gaps_on_consecutive_sessions(tmp_path, provider):
    summary = run(
        ["KO"],
        "2021-06-01",
        "2021-06-10",
        out_dir=tmp_path / "d",
        reports_dir=tmp_path / "r",
        use_cache=False,
        provider=provider,
    )
    assert summary["tickers"]["KO"]["missing_sessions"] == 0


def test_provider_invoked_offline_with_auto_adjust_false(tmp_path, provider):
    run(["KO"], "2021-06-01", "2021-06-10", out_dir=tmp_path / "d", reports_dir=tmp_path / "r",
        use_cache=False, provider=provider)
    assert provider.calls, "provider should have been called"
    assert provider.calls[0][-1] == "auto_adjust=False"


def test_unknown_ticker_returns_empty_summary(tmp_path):
    from tests.conftest import FakeProvider

    summary = run(
        ["NOPE"],
        "2021-06-01",
        "2021-06-10",
        out_dir=tmp_path / "d",
        reports_dir=tmp_path / "r",
        use_cache=False,
        provider=FakeProvider({}),
    )
    assert summary["n_tickers"] == 0


def test_parser_defaults():
    args = build_parser().parse_args([])
    assert args.tickers == ["SPY", "KO", "AAPL"]
    assert args.calendar == "NYSE"
