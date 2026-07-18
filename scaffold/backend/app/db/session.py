"""SQLAlchemy engine/session setup.

The engine is created lazily so importing this module (e.g. during tests) never requires a
live Postgres. Call `get_engine()` / `init_db()` at application startup.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import settings

Base = declarative_base()

_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    """Return a process-wide SQLAlchemy engine, creating it on first use."""
    global _engine
    if _engine is None:
        _engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
    return _engine


def get_sessionmaker() -> sessionmaker:
    """Return a process-wide sessionmaker bound to the engine."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, future=True)
    return _SessionLocal


def init_db() -> None:
    """Create all tables. Safe to call repeatedly (idempotent)."""
    from . import models  # noqa: F401  (register models on Base)

    Base.metadata.create_all(bind=get_engine())


def get_db():
    """FastAPI dependency yielding a scoped session."""
    session = get_sessionmaker()()
    try:
        yield session
    finally:
        session.close()
