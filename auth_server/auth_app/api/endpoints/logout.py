from fastapi import APIRouter, status, Response, Depends
from auth_app.api import token_deps
router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, dependencies=[Depends(token_deps.exist_access_token)])
async def logout(
    response: Response,
) -> dict:
    """
    jwt 토큰 삭제
    """
    response.delete_cookie(key='access_token')
    return {"message": "Delete Cookie Token"}
