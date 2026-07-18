"""FastAPI application entrypoint for MERIDIAN.

Wires the REST and WebSocket routers. DB tables are created on startup best-effort — the app
still boots (and the simulation still runs in-memory) if Postgres is unavailable, so the
scaffold is usable without Docker.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from .api.routes_simulation import router as simulation_router
from .api.routes_ws import router as ws_router
from .config import settings

logger = logging.getLogger("meridian")

app = FastAPI(
    title="MERIDIAN — Synthetic Society Crisis Simulator",
    version="0.1.0",
    description="Runnable scaffold. LLM layer stubbed; runs with no API keys.",
)

app.include_router(simulation_router)
app.include_router(ws_router)


@app.on_event("startup")
def on_startup() -> None:
    """Create DB tables if a database is reachable; otherwise continue in-memory."""
    try:
        from .db.session import init_db

        init_db()
        logger.info("Database initialised.")
    except Exception as exc:  # noqa: BLE001 - scaffold should boot without a DB
        logger.warning("DB init skipped (%s). Running in-memory only.", exc)


@app.get("/health")
def health() -> dict:
    """Liveness probe."""
    return {"status": "ok", "llm_mode": settings.llm_mode}
