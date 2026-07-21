"""FastAPI application entrypoint for MERIDIAN.

Wires the REST and WebSocket routers. DB tables are created on startup best-effort — the app
still boots (and the simulation still runs in-memory) if Postgres is unavailable, so the
scaffold is usable without Docker.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from .api.routes_simulation import router as simulation_router
from .api.routes_demo import router as demo_router
from .api.routes_belief import router as belief_router
from .api.routes_virtual_person import router as virtual_person_router
from .api.routes_ask import router as ask_router
from .api.routes_ws import router as ws_router
from .config import settings

logger = logging.getLogger("meridian")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MERIDIAN — Simulated-Society Crisis Simulator",
    version="0.1.0",
    description=(
        "Runnable scaffold. The LLM layer is a stub that calls no model and needs no API "
        "keys. One cross-tier societal-response mechanism is implemented (P0.5); nothing "
        "is persisted and there is no replay."
    ),
)

# Local development only: the Vite dev server runs on a different port. This is not a
# production CORS policy and no auth boundary exists behind it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(simulation_router)
app.include_router(demo_router)
app.include_router(belief_router)
app.include_router(virtual_person_router)
app.include_router(ask_router)
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
