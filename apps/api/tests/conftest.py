"""Shared pytest fixtures.

The `db` fixture skips DB-backed tests when Postgres is unreachable, so the
no-DB unit tests still run anywhere. It creates tables directly from metadata
(migrations are exercised separately via `alembic upgrade`).
"""

from __future__ import annotations

import pytest
from sqlalchemy import text

from app.db.base import Base
from app.db.session import engine


@pytest.fixture(scope="session")
def db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - any connection failure -> skip
        pytest.skip(f"database not available: {exc}")
    Base.metadata.create_all(engine)
    yield
