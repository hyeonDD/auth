import redis.asyncio as redis
from jose import JWTError, jwt

from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

from auth_app.core.config import settings

import auth_app.schemas.redis as redis_schemas
from auth_app.api import redis_deps
from auth_app.api import token_deps
from auth_app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/access-token", status_code=status.HTTP_200_OK)
async def login_access_token(
    response: Response,
    *,
    redis_db: redis.Redis = Depends(redis_deps.get_redis_db),
    user_in: redis_schemas.UserLogin,
) -> dict:
    """
    로그인 로직
    """

    login_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
        "error": "Not Found",
        "message": "The user does not exist on this system or the password is incorrect.",
    })
    # email, password 빈칸 확인
    if not user_in.email or not user_in.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "error": "Bad Request",
            "message": "There is no email or password field",
        })

    # 입력받은 email, password 확인
    check_user = await redis_db.get(user_in.email)

    # 없는 user로 로그인 했을때
    if not check_user:
        raise login_exception

    # 비밀번호가 틀렸을때
    # register app 에서 hset말고 그냥 set 해서 문자열로 넘어와져서 json -> pydantic 모델
    user_info = redis_schemas.RedisUser.model_validate_json(check_user)

    if not verify_password(user_in.password, user_info.password):
        raise login_exception

    # jwt 토큰 생성
    payload = user_info.model_dump(exclude={'password'})

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        payload,
        expire_minutes=access_token_expires
    )

    # 쿠키 설정
    response.set_cookie(key="access_token", value=access_token,
                        httponly=True, expires=datetime.now(timezone.utc)+access_token_expires)

    return {"message": "Sucess Login User"}


@router.get("/check", status_code=status.HTTP_200_OK, dependencies=[Depends(token_deps.exist_access_token)])
async def verify_access_token(
    request: Request,
) -> dict:
    """
    token 위변조 체크용
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        jwt.decode(
            request.cookies['access_token'], settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
    except JWTError:
        raise credentials_exception

    return {"message": "Sucess Validate Token"}
