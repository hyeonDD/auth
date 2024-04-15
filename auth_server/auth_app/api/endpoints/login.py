import redis.asyncio as redis

from fastapi import APIRouter, Depends, HTTPException

from auth_app.core.config import settings

import auth_app.schemas.redis as redis_schemas
import auth_app.crud.redis as redis_crud
from auth_app.api import redis_deps
from auth_app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/access-token", status_code=201)
async def login_access_token(
    *,
    redis_db: redis.Redis = Depends(redis_deps.get_redis_db),
    user_in: redis_schemas.UserLogin,
) -> dict:
    """
    로그인 로직
    """

    # email, password 빈칸 확인
    if not user_in.email or not user_in.password:
        raise HTTPException(status_code=422, detail={
            "error": "Bad Request",
            "message": "There is no email or password field",
        })

    # 입력받은 email, password 확인
    check_user = await redis_db.get(user_in.email)

    # 없는 user로 로그인 했을때
    if not check_user:
        raise HTTPException(status_code=404, detail={
            "error": "Not Found",
            "message": "The user does not exist on this system or the password is incorrect.",
        })

    # 비밀번호가 틀렸을때
    #  register app 에서 hset말고 그냥 set 해서 문자열로 넘어와져서 json -> pydantic 모델
    user_info = redis_schemas.RedisUser.model_validate_json(check_user)

    if not verify_password(user_in.password, user_info.password):
        raise HTTPException(status_code=404, detail={
            "error": "Not Found",
            "message": "The user does not exist on this system or the password is incorrect.",
        })

    payload = user_info.model_dump(exclude={'password'})

    return {
        "access_token": create_access_token(
            payload,
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "token_type": "bearer",  # OAuth를 나타내는 인증 타입
    }
