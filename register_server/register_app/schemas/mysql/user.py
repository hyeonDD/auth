from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    공통 속성
    """
    email: EmailStr
    password: str


class UserCreate(UserBase):
    """
    유저 등록
    """
    nickname: str
