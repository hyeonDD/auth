from pydantic import BaseModel, EmailStr


class RedisUser(BaseModel):
    email: EmailStr
    nickname: str
    password: str
    permission: str
