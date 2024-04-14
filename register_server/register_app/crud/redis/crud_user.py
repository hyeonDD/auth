import redis.asyncio as redis
from pydantic import BaseModel


async def create_cache(db: redis.Redis, *, key: str, value: BaseModel) -> None:
    """
    redis cache 만들기
    """
    await db.set(key, value.model_dump_json())
