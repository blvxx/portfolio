"""Environment-based application settings."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _optional_int(name: str) -> int | None:
    value = os.getenv(name, "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer Telegram ID") from exc


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    database_path: str = "data/leads.sqlite3"
    admin_chat_id: int | None = None
    admin_user_id: int | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError(
                "BOT_TOKEN is missing. Copy .env.example to .env and add your token."
            )

        return cls(
            bot_token=token,
            database_path=os.getenv("DATABASE_PATH", "data/leads.sqlite3").strip(),
            admin_chat_id=_optional_int("ADMIN_CHAT_ID"),
            admin_user_id=_optional_int("ADMIN_USER_ID"),
        )
