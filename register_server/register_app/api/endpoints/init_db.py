from fastapi import APIRouter
from sqlalchemy import insert, select
import redis.asyncio as redis

from register_app.db.mysql.base_class import Base
from register_app.db.mysql.session import engine
from register_app.models.mysql.user import User
from register_app.core.security import get_password_hash
from register_app.core.config import settings
from register_app.crud.redis import create_cache

router = APIRouter()


@router.post("/", status_code=201)
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(insert(User).values(nickname='superuser', email='superuser@example.com', password=get_password_hash('1'), permission='superuser'))
        result = await conn.execute(select(User).filter(User.email == 'superuser@example.com'))
        result = result.first()
    redis_client = redis.Redis.from_url(settings.REDIS_URL)
    await create_cache(redis_client, key=result.email, value=result.id)
    return {"message": "User DB Table and Colum, Redis Cache Create Successful"}


@router.delete("/", status_code=200)
async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    redis_client = redis.Redis.from_url(settings.REDIS_URL)
    await redis_client.flushall()

    return {"message": "User DB Table and Colum, Redis Cache Delete Successful"}
