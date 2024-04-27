import base64
from fastapi import HTTPException, status, Request
import blog_app.schemas.token as token_schemas


def exist_access_token(request: Request) -> str:
    """
    access token 유/무 확인
    """
    if not request.cookies.get('access_token'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Access token not found in cookie")
    _, base64_payload, _ = request.cookies.get('access_token').split('.')
    padding_len = len(base64_payload) % 4
    base64_payload += '=' * padding_len
    return base64_payload


def get_user(request: Request) -> token_schemas.Payload:
    # 토큰있는지 확인
    base64_payload = exist_access_token(request)
    # superuser 확인
    decoded_payload = base64.b64decode(base64_payload)
    decoded_string = decoded_payload.decode('utf-8')
    # json string -> pydantic model 변환
    payload = token_schemas.Payload.model_validate_json(decoded_string)
    return payload


def is_superuser(request: Request) -> None:
    """
    superuser인지 확인
    """
    payload = get_user(request)
    if payload.permission != 'superuser':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="The user doesn't have enough privileges")
