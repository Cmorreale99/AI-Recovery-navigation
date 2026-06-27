"""FastAPI application entrypoint.

Phase 1 wires up only the app, CORS, and the `/health` route. Subsequent phases
register routers for intake, journal, documents, extraction, safety, artifacts,
tracker, and export under this same app.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import consent, health, intake, users
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(consent.router)
app.include_router(intake.router)
