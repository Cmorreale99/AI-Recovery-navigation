"""Application configuration loaded from environment variables.

Secrets and connection strings never live in code — see `.env.example` for the
full set of supported variables. The app is local-first and must run end-to-end
with no LLM API key (mock mode is the default).
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI Recovery Navigation API"
    environment: str = "development"

    # Infrastructure
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/recovery"
    redis_url: str = "redis://redis:6379/0"

    # LLM / embeddings. Absent key => deterministic mock mode (Phase 5).
    llm_provider: str = "mock"
    llm_api_key: str | None = None
    embeddings_provider: str = "mock"

    # CORS: the Next.js dev server origin(s) allowed to call the API.
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
