"""Integration tests for Redis-backed FSM persistence across instances."""

import os
import uuid

import pytest
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.state import State
from redis.asyncio import Redis

from src.states import RequestFlow


REDIS_URL = os.getenv("REDIS_URL")
pytestmark = pytest.mark.skipif(not REDIS_URL, reason="REDIS_URL is not configured")


@pytest.mark.asyncio
async def test_fsm_state_survives_storage_reconnect_and_is_shared() -> None:
    assert REDIS_URL is not None
    key = StorageKey(
        bot_id=910001,
        chat_id=920000 + uuid.uuid4().int % 100000,
        user_id=930001,
    )
    redis_one = Redis.from_url(REDIS_URL, decode_responses=True)
    redis_two = Redis.from_url(REDIS_URL, decode_responses=True)
    first = RedisStorage(redis=redis_one)
    second = RedisStorage(redis=redis_two)

    try:
        await first.set_state(key, RequestFlow.waiting_contact)
        await first.set_data(key, {"selected_service": "Support"})

        assert await second.get_state(key) == RequestFlow.waiting_contact.state
        assert await second.get_data(key) == {"selected_service": "Support"}

        await first.close()
        first = RedisStorage(
            redis=Redis.from_url(REDIS_URL, decode_responses=True)
        )
        assert await first.get_state(key) == RequestFlow.waiting_contact.state
        assert await first.get_data(key) == {"selected_service": "Support"}
    finally:
        await first.set_state(key, None)
        await first.set_data(key, {})
        await first.close()
        await second.close()
