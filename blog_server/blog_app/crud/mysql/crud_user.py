from pydantic import EmailStr

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from register_app.core.security import get_password_hash, verify_password
from register_app.models.mysql.user import User
from register_app.schemas.mysql.user import UserCreate


async def is_exist_user(db: AsyncSession, email: EmailStr, nickname: str) -> bool:
    """
    이미 있는 유저인지 확인
    """
    query = select(User).filter(or_(User.email == email,
                                User.nickname == nickname)).limit(1)
    result = await db.execute(query)
    is_exist = True if result.scalar() else False
    return is_exist


async def create_user(db: AsyncSession, *, obj_in: UserCreate) -> User:
    """
    유저 만들기
    """
    db_obj = User(
        email=obj_in.email,
        password=get_password_hash(obj_in.password),
        nickname=obj_in.nickname,
        permission=obj_in.permission,
    )
    db.add(db_obj)
    await db.commit()
    return db_obj
