from typing import Annotated
from fastapi import Cookie, HTTPException, status


def exist_access_token(access_token: Annotated[str, Cookie()]):
    """
    access token 유/무 확인
    """
