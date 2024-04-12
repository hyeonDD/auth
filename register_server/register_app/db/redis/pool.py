import redis.asyncio as redis

from register_app.core.config import settings


pool = redis.ConnectionPool.from_url(settings.REDIS_URL)
