from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class PostBase(BaseModel):
    """
    공통 속성
    """
    email: EmailStr
    nickname: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class PostCreate(PostBase):
    """
    글 등록
    """
    nickname: str
    title: str = Field(min_length=8, max_length=50)
    description: str = Field(min_length=10, max_length=500)
