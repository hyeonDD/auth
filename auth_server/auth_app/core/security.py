from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from auth_app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    패스워드 해시화
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    패스워드 해시 확인용
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expire_minutes: timedelta) -> str:
    """ 
    JWT 토큰 생성 후 반환
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expire_minutes
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt
