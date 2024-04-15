import redis.asyncio as redis

from auth_app.core.config import settings


pool = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)
