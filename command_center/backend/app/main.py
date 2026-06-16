"""FastAPI app factory. Serves /api/v1 and (in prod) the built SPA from frontend/dist."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .middleware import TimingMiddleware
from .routers import analytics, catalog, meta, ohlcv


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="command_center",
        version="0.1.0",
        description="Bloomberg-style research terminal API over quant_core.",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["x-response-time-ms"],
    )
    app.add_middleware(TimingMiddleware)

    @app.get("/healthz", operation_id="healthz", tags=["health"])
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    for module in (meta, catalog, ohlcv, analytics):
        app.include_router(module.router, prefix="/api/v1")

    if settings.frontend_dist and settings.frontend_dist.is_dir():
        from fastapi.staticfiles import StaticFiles

        app.mount("/", StaticFiles(directory=str(settings.frontend_dist), html=True), name="spa")

    return app


app = create_app()
