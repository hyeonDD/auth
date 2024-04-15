from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserLogin(UserBase):
    """
    사용자 로그인
    """
    ...


class RedisUser(UserBase):
    """
    사용자 스키마
    """
    nickname: str
    permission: str
    nickname: str
    permission: str
