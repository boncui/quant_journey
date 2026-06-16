"""Offline API tests — routing, serialization, the catalog, and ticker-input validation."""

from __future__ import annotations


def test_healthz(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_meta_reports_versions_and_sources(client):
    j = client.get("/api/v1/meta").json()
    assert j["api"] == "v1"
    assert j["quant_core_version"]
    assert "seed" in j["sources"]


def test_catalog_lists_seeded_universe(client):
    j = client.get("/api/v1/catalog").json()
    assert j["empty"] is False
    assert {"SPY", "KO", "AAPL"}.issubset(set(j["universe"]))
    assert all(item["source"] == "seed" for item in j["items"])


def test_response_has_timing_header(client):
    r = client.get("/api/v1/catalog")
    assert "x-response-time-ms" in {k.lower() for k in r.headers}


def test_ohlcv_returns_bars_from_seed(client):
    j = client.get("/api/v1/ohlcv/AAPL").json()
    assert j["ticker"] == "AAPL"
    assert len(j["bars"]) > 0
    assert j["meta"]["source"] == "seed"
    bar = j["bars"][0]
    assert bar["h"] >= bar["low"]


def test_ohlcv_rejects_invalid_ticker(client):
    assert client.get("/api/v1/ohlcv/a$b").status_code == 422


def test_returns_and_distribution(client):
    assert len(client.get("/api/v1/returns/AAPL?kind=log").json()["series"]) > 0
    d = client.get("/api/v1/distribution/AAPL").json()
    assert d["moments"]["n"] > 0
    assert len(d["histogram"]["counts"]) > 0


def test_rolling_vol(client):
    j = client.get("/api/v1/rolling/AAPL?window=21&stat=vol").json()
    assert j["stat"] == "vol"
    assert len(j["series"]) > 0


def test_performance_overlay_is_rebased_to_100(client):
    j = client.get("/api/v1/performance?tickers=SPY,KO,AAPL&base=100").json()
    assert len(j["series"]) == 3
    first_point = j["series"][0]["points"][0]
    assert abs(first_point["v"] - 100.0) < 1e-6


def test_correlation_matrix_diagonal(client):
    j = client.get("/api/v1/correlation?tickers=SPY,KO,AAPL").json()
    assert len(j["matrix"]) == 3
    assert abs(j["matrix"][0][0] - 1.0) < 1e-6


def test_beta(client):
    j = client.get("/api/v1/beta/AAPL?benchmark=SPY").json()
    assert j["n"] > 0
    assert j["beta"] is not None


def test_coverage_and_corporate_actions(client):
    cov = client.get("/api/v1/catalog/AAPL/coverage").json()
    assert cov[0]["ticker"] == "AAPL"
    ca = client.get("/api/v1/corporate-actions/KO").json()
    assert "adj_factor" in ca
