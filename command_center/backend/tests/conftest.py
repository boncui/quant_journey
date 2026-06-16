"""Offline backend fixtures: a fake repo + a synthetic seed dir, injected via dependency_overrides.

No network, no real cache — mirrors quant_core's offline-fixture discipline.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from quant_core.data import make_synthetic_ohlcv

from app.config import Settings, get_settings
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    repo = tmp_path / "repo"
    seed = tmp_path / "seed"
    cache = tmp_path / "cache"
    for d in (repo, seed, cache):
        d.mkdir()

    df = make_synthetic_ohlcv(["SPY", "KO", "AAPL"], "2020-01-01", "2021-06-01")
    for ticker in df["ticker"].cat.categories:
        block = df[df["ticker"] == ticker]
        block.to_parquet(seed / f"{ticker}_1d.parquet", index=False)

    settings = Settings(repo_root=repo, cache_dir=cache, seed_dir=seed)
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    return TestClient(app)
