import redis.asyncio as redis
from typing import AsyncIterator

from register_app.db.redis.pool import pool


async def get_redis_db() -> AsyncIterator:
    async with redis.Redis.from_pool(pool) as db:
        yield db
