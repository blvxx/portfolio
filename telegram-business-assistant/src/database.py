"""SQLite persistence for incoming enquiries and the notification outbox."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import aiosqlite


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _timestamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds")


class Database:
    """Single-file SQLite adapter.

    Lead creation and outbox event creation share one SQLite transaction.
    Notification delivery is at-least-once: a worker lease can expire after a
    successful remote send but before the local delivered marker is committed.
    """

    def __init__(self, path: str) -> None:
        self.path = path

    async def _configure(self, connection: aiosqlite.Connection) -> None:
        await connection.execute("PRAGMA foreign_keys = ON")
        await connection.execute("PRAGMA busy_timeout = 5000")

    async def initialize(self) -> None:
        if self.path != ":memory:":
            Path(self.path).expanduser().parent.mkdir(parents=True, exist_ok=True)

        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
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
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notification_outbox (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    aggregate_id INTEGER NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
                    payload_json TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'processing', 'delivered', 'dead')),
                    attempts INTEGER NOT NULL DEFAULT 0,
                    available_at TEXT NOT NULL,
                    locked_at TEXT,
                    last_error TEXT,
                    created_at TEXT NOT NULL,
                    delivered_at TEXT,
                    UNIQUE(event_type, aggregate_id)
                )
                """
            )
            await connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_outbox_due
                ON notification_outbox(status, available_at, locked_at)
                """
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
        admin_chat_id: int | None = None,
    ) -> int:
        """Persist a lead and, when configured, its notification event atomically."""
        now = _timestamp(_utc_now())
        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
            await connection.execute("BEGIN IMMEDIATE")
            try:
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
                        now,
                    ),
                )
                lead_id = int(cursor.lastrowid)

                if admin_chat_id is not None:
                    await connection.execute(
                        """
                        INSERT INTO notification_outbox (
                            event_type, aggregate_id, payload_json,
                            status, attempts, available_at, created_at
                        )
                        VALUES (?, ?, ?, 'pending', 0, ?, ?)
                        """,
                        (
                            "lead.created",
                            lead_id,
                            json.dumps({"chat_id": admin_chat_id}),
                            now,
                            now,
                        ),
                    )

                await connection.commit()
                return lead_id
            except Exception:
                await connection.rollback()
                raise

    async def get_recent_leads(self, limit: int = 10) -> list[dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 50))
        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
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

    async def claim_notification(
        self, *, lease_seconds: int = 60
    ) -> dict[str, Any] | None:
        """Atomically claim one due event, reclaiming expired worker leases."""
        now = _utc_now()
        now_text = _timestamp(now)
        stale_before = _timestamp(now - timedelta(seconds=max(1, lease_seconds)))

        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
            connection.row_factory = aiosqlite.Row
            await connection.execute("BEGIN IMMEDIATE")
            try:
                cursor = await connection.execute(
                    """
                    SELECT id
                    FROM notification_outbox
                    WHERE
                        (status = 'pending' AND available_at <= ?)
                        OR
                        (status = 'processing' AND locked_at <= ?)
                    ORDER BY id ASC
                    LIMIT 1
                    """,
                    (now_text, stale_before),
                )
                candidate = await cursor.fetchone()
                if candidate is None:
                    await connection.commit()
                    return None

                event_id = int(candidate["id"])
                await connection.execute(
                    """
                    UPDATE notification_outbox
                    SET status = 'processing',
                        locked_at = ?,
                        attempts = attempts + 1
                    WHERE id = ?
                    """,
                    (now_text, event_id),
                )
                cursor = await connection.execute(
                    """
                    SELECT
                        o.id AS notification_id,
                        o.aggregate_id AS lead_id,
                        o.payload_json,
                        o.attempts,
                        l.telegram_user_id,
                        l.username,
                        l.customer_name,
                        l.contact,
                        l.service,
                        l.details,
                        l.created_at
                    FROM notification_outbox AS o
                    JOIN leads AS l ON l.id = o.aggregate_id
                    WHERE o.id = ?
                    """,
                    (event_id,),
                )
                row = await cursor.fetchone()
                await connection.commit()
                if row is None:
                    return None

                event = dict(row)
                payload = json.loads(event.pop("payload_json"))
                event["chat_id"] = int(payload["chat_id"])
                return event
            except Exception:
                await connection.rollback()
                raise

    async def mark_notification_delivered(self, notification_id: int) -> None:
        now = _timestamp(_utc_now())
        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
            cursor = await connection.execute(
                """
                UPDATE notification_outbox
                SET status = 'delivered',
                    delivered_at = ?,
                    locked_at = NULL,
                    last_error = NULL
                WHERE id = ? AND status = 'processing'
                """,
                (now, notification_id),
            )
            await connection.commit()
            if cursor.rowcount != 1:
                raise RuntimeError("Notification event is no longer leased by this worker")

    async def reschedule_notification(
        self,
        notification_id: int,
        *,
        error_code: str,
        max_attempts: int = 5,
        base_delay_seconds: int = 5,
    ) -> str:
        """Schedule exponential retry or move an exhausted event to the dead state."""
        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
            cursor = await connection.execute(
                "SELECT attempts, status FROM notification_outbox WHERE id = ?",
                (notification_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                raise ValueError(f"Unknown notification event: {notification_id}")
            if row[1] != "processing":
                raise RuntimeError("Notification event is not currently leased")

            attempts = int(row[0])
            now = _utc_now()
            if attempts >= max(1, max_attempts):
                status = "dead"
                available_at = _timestamp(now)
            else:
                status = "pending"
                delay = min(3600, max(0, base_delay_seconds) * (2 ** (attempts - 1)))
                available_at = _timestamp(now + timedelta(seconds=delay))

            await connection.execute(
                """
                UPDATE notification_outbox
                SET status = ?,
                    available_at = ?,
                    locked_at = NULL,
                    last_error = ?
                WHERE id = ? AND status = 'processing'
                """,
                (status, available_at, error_code[:80], notification_id),
            )
            await connection.commit()
            return status

    async def get_notification_event(
        self, notification_id: int
    ) -> dict[str, Any] | None:
        """Return outbox metadata for tests and operational inspection."""
        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(
                """
                SELECT id, event_type, aggregate_id, status, attempts,
                       available_at, locked_at, last_error, created_at, delivered_at
                FROM notification_outbox
                WHERE id = ?
                """,
                (notification_id,),
            )
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_notification_for_lead(
        self, lead_id: int
    ) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.path) as connection:
            await self._configure(connection)
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(
                """
                SELECT id, status, attempts
                FROM notification_outbox
                WHERE aggregate_id = ? AND event_type = 'lead.created'
                """,
                (lead_id,),
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
