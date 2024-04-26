from pydantic import BaseModel, EmailStr


class Payload(BaseModel):
    email: EmailStr
    nickname: str
    permission: str
    exp: int
