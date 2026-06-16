# command_center / backend

FastAPI viz/serialization layer over `quant_core`. It hosts **no** quant math — every analytic
lives in `quant_core` and is exposed here over a typed, downsampled, tested HTTP contract under
`/api/v1`. See [`../METAPROMPT.md`](../METAPROMPT.md) for the operating charter.

```bash
# from the repo root
make cc-setup          # uv sync this backend (+ editable quant_core[stats]) and the frontend
make cc-seed           # write deterministic synthetic OHLCV so the catalog/charts have data offline
uv run --directory command_center/backend uvicorn app.main:app --reload --port 8000
uv run --directory command_center/backend pytest          # offline tests
uv run --directory command_center/backend python -m app.openapi_dump   # write openapi.json
```

Data access goes through the single seam `app.deps.load_ohlcv` (swap to DuckDB later without
touching routes). On a fresh clone with no data, endpoints fall back to in-memory synthetic data
(`CC_ALLOW_SYNTHETIC=1`, the default) so the terminal is never blank; `make cc-seed` makes that data
show up in the catalog too. Configuration is via `CC_`-prefixed env vars (see `app/config.py`).
