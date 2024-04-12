import redis.asyncio as redis


async def create_cache(db: redis.Redis, *, key: str, value: dict) -> None:
    """
    redis cache 만들기
    """
    await db.set(key, value)
