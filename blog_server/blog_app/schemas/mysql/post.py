from typing import Optional, Annotated
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from fastapi import HTTPException


class PostBase(BaseModel):
    """
    공통 속성
    """
    title: Optional[str] = None
    description: Optional[str] = None


class PostCreate(PostBase):
    """
    글 등록
    """
    title: str = Field(min_length=8, max_length=50)
    description: str = Field(min_length=10, max_length=500)


class PostUpdate(PostBase):
    """
    글 수정
    """
    title: str = Field(min_length=8, max_length=50)
    description: str = Field(min_length=10, max_length=500)


"""
class PostDTO(PostBase):
    """
# 글 dto
"""
    id: str
    email: EmailStr
    title: str = Field(min_length=8, max_length=50)
    description: str = Field(min_length=10, max_length=500)
    # update_at: datetime = datetime.now(timezone.utc)
    create_at = Annotated[datetime, "작성시간"]
    update_at: datetime = datetime.now(timezone.utc)

    # v1의 orm_mode가 ConfigDict읭 from_attributes=True
    # model_config = ConfigDict(from_attributes=True)
"""
