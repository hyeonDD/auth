from fastapi import HTTPException, status, Request


def exist_access_token(request: Request):
    """
    access token 유/무 확인
    """
    if not request.cookies.get('access_token'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Access token not found in cookie")
