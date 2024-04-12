from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from register_app.core.config import settings
from register_app.api import mysql_deps
import register_app.crud.mysql as mysql_crud
import register_app.schemas.mysql as schemas

import register_app.crud.redis as redis_crud
from register_app.api import redis_deps

router = APIRouter()


@router.post("/", status_code=201)
async def create_user(
    *,
    superuser_header: str = Header(None),
    mysql_db: AsyncSession = Depends(mysql_deps.get_mysql_db),
    redis_db: AsyncSession = Depends(redis_deps.get_redis_db),
    user_in: schemas.UserCreate,
) -> dict:
    """
    새로운 유저 만드는 기능
    """

    if superuser_header != settings.SUPERUSER_HEADER:
        raise HTTPException(status_code=401, detail={
            "error": "Unauthorized user",
            "message": "You do not have permission",
        })

    is_exist_user = await mysql_crud.is_exist_user(mysql_db, email=user_in.email, nickname=user_in.nickname)

    if is_exist_user:
        raise HTTPException(status_code=409, detail={
            "error": "User already exists",
            "message": "The user with the provided nickname or email already exists."
        })

    result_mysql = await mysql_crud.create_user(mysql_db, obj_in=user_in)

    await redis_crud.create_cache(redis_db, key=result_mysql.email, value=str(result_mysql.id))

    return {"message": "User Create Successful"}
