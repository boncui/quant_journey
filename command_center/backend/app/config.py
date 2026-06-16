"""Settings — all configuration via ``CC_``-prefixed env vars (or an .env file)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from quant_core.data.cache import DEFAULT_CACHE_DIR

_BACKEND_DIR = Path(__file__).resolve().parents[1]      # .../command_center/backend
_REPO_ROOT = Path(__file__).resolve().parents[3]        # .../quant_journey


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CC_", env_file=".env", extra="ignore")

    repo_root: Path = _REPO_ROOT
    cache_dir: Path = DEFAULT_CACHE_DIR
    seed_dir: Path = _BACKEND_DIR / ".cc_seed"          # `make cc-seed` writes synthetic parquet here

    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    max_series_points: int = 4000                        # downsample threshold for the wire

    # Fresh-clone friendliness: when no on-disk dataset matches, serve deterministic synthetic data
    # so the terminal is never blank. Set CC_ALLOW_SYNTHETIC=0 to force real-data-only.
    allow_synthetic: bool = True
    default_universe: list[str] = ["SPY", "KO", "AAPL"]
    default_start: str = "2018-01-01"
    default_end: str = "2024-01-01"

    # Set to the built SPA dir (command_center/frontend/dist) to serve the UI from FastAPI in prod.
    frontend_dist: Path | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
