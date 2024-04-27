from pydantic import EmailStr
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from blog_app.models.mysql.post import Post
from blog_app.schemas.mysql.post import PostCreate, PostUpdate  # PostDTO


async def create_with_owner(db: AsyncSession, *, user_in: PostCreate, email: EmailStr) -> Post:
    """
    email 포함하여 글작성
    """
    db_obj = Post(email=email, title=user_in.title,
                  description=user_in.description)
    db.add(db_obj)
    await db.commit()
    return db_obj


async def get_multi_by_owner(db: AsyncSession, *, email: EmailStr, skip: int = 0, limit: int = 100) -> List[Post]:
    """
    입력 email이 쓴 글들 조회
    """
    query = select(Post).filter(Post.email ==
                                email).offset(skip).limit(limit)
    result = await db.execute(query)
    data = result.scalars().all()
    return data


"""
async def update(db: AsyncSession, *, db_obj: Post, obj_in: PostUpdate,) -> Post:
    obj_data = PostDTO.model_validate(db_obj)

    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    return db_obj


async def delet():
    ...
"""
