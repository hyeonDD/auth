from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from blog_app.api import mysql_deps
from blog_app.api import authorization_deps
from blog_app.crud.mysql import crud_post
import blog_app.schemas.mysql as post_schemas
import blog_app.schemas.token as token_schemas


router = APIRouter()


@router.post("/", status_code=201)
async def create_post(
    *,
    get_user: token_schemas.Payload = Depends(authorization_deps.get_user),
    mysql_db: AsyncSession = Depends(mysql_deps.get_mysql_db),
    user_in: post_schemas.PostCreate,
) -> dict:
    """
    새로운 글 만드는 기능
    """

    await crud_post.create_with_owner(mysql_db, user_in=user_in, email=get_user.email)

    return {"message": "Post Create Successful"}
