"""SQLite persistence for incoming business enquiries."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiosqlite


class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    async def initialize(self) -> None:
        if self.path != ":memory:":
            Path(self.path).expanduser().parent.mkdir(parents=True, exist_ok=True)

        async with aiosqlite.connect(self.path) as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_user_id INTEGER NOT NULL,
                    username TEXT,
                    customer_name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    service TEXT NOT NULL,
                    details TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            await connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at)"
            )
            await connection.commit()

    async def add_lead(
        self,
        *,
        telegram_user_id: int,
        username: str | None,
        customer_name: str,
        contact: str,
        service: str,
        details: str,
    ) -> int:
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        async with aiosqlite.connect(self.path) as connection:
            cursor = await connection.execute(
                """
                INSERT INTO leads (
                    telegram_user_id, username, customer_name, contact,
                    service, details, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    telegram_user_id,
                    username,
                    customer_name,
                    contact,
                    service,
                    details,
                    created_at,
                ),
            )
            await connection.commit()
            return int(cursor.lastrowid)

    async def get_recent_leads(self, limit: int = 10) -> list[dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 50))
        async with aiosqlite.connect(self.path) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(
                """
                SELECT id, telegram_user_id, username, customer_name,
                       contact, service, details, created_at
                FROM leads
                ORDER BY id DESC
                LIMIT ?
                """,
                (safe_limit,),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
