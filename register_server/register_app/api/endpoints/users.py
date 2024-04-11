from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from register_app.api import mysql_deps
import register_app.crud.mysql as mysql_crud
import register_app.schemas.mysql as schemas

router = APIRouter()


@router.post("/", status_code=201)
async def create_user(
    *,
    db: AsyncSession = Depends(mysql_deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    새로운 유저 만드는 기능
    """

    is_exist_user = await mysql_crud.is_exist_user(db, email=user_in.email, nickname=user_in.nickname)
    print(is_exist_user)
    if is_exist_user:
        raise HTTPException(status_code=409, detail={
            "error": "User already exists",
            "message": "The user with the provided nickname or email already exists."
        })

    await mysql_crud.create_user(db, obj_in=user_in)

    return {"message": "User Create Successful"}
