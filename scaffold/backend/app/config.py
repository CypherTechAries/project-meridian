"""Application settings, loaded from environment / .env (pydantic-settings)."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo root: backend/app/config.py -> parents[2] == scaffold/
REPO_ROOT = Path(__file__).resolve().parents[2]
SCENARIOS_DIR = REPO_ROOT / "scenarios"


class Settings(BaseSettings):
    """Runtime configuration. All values have safe local defaults."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://meridian:meridian@localhost:5432/meridian"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # LLM gateway: "stub" (default, no keys) or "live" (wire LiteLLM).
    llm_mode: str = "stub"
    llm_model: str = "anthropic/claude-opus-4-7"

    default_seed: int = 88213


settings = Settings()
