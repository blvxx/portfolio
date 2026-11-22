"""Health, readiness and Prometheus endpoints for the runtime."""

import logging
from typing import Any

from aiohttp import web
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.metrics import (
    OUTBOX_DEAD,
    OUTBOX_DELIVERED,
    OUTBOX_PENDING,
    OUTBOX_PROCESSING,
)

logger = logging.getLogger(__name__)


def create_observability_app(database: Any, redis_client: Any | None = None) -> web.Application:
    """Create an aiohttp app exposing liveness, dependency readiness and metrics."""

    app = web.Application()

    async def healthz(_request: web.Request) -> web.Response:
        return web.json_response({"status": "ok"})

    async def readyz(_request: web.Request) -> web.Response:
        try:
            await database.ping()
            if redis_client is not None:
                await redis_client.ping()
        except Exception as exc:
            logger.warning(
                "Readiness probe failed",
                extra={"error_type": type(exc).__name__},
            )
            return web.json_response({"status": "not_ready"}, status=503)
        return web.json_response({"status": "ready"})

    async def metrics(_request: web.Request) -> web.Response:
        try:
            stats = await database.get_notification_stats()
            OUTBOX_PENDING.set(stats["pending"])
            OUTBOX_PROCESSING.set(stats["processing"])
            OUTBOX_DELIVERED.set(stats["delivered"])
            OUTBOX_DEAD.set(stats["dead"])
        except Exception as exc:
            logger.warning(
                "Outbox metrics refresh failed",
                extra={"error_type": type(exc).__name__},
            )
        return web.Response(
            body=generate_latest(),
            headers={"Content-Type": CONTENT_TYPE_LATEST},
        )

    app.router.add_get("/healthz", healthz)
    app.router.add_get("/readyz", readyz)
    app.router.add_get("/metrics", metrics)
    return app
