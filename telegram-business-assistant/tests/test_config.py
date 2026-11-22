"""Configuration contract tests for horizontally-scalable deployment mode."""

import pytest

from src.config import Settings


def test_webhook_mode_requires_postgres_and_redis(monkeypatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("BOT_MODE", "webhook")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.setenv("WEBHOOK_BASE_URL", "https://bot.example.com")
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret")

    with pytest.raises(ValueError, match="PostgreSQL"):
        Settings.from_env()


def test_webhook_mode_requires_public_https_endpoint(monkeypatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("BOT_MODE", "webhook")
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql://assistant:secret@localhost:5432/assistant"
    )
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("WEBHOOK_BASE_URL", "http://bot.example.com")
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret")

    with pytest.raises(ValueError, match="HTTPS"):
        Settings.from_env()
