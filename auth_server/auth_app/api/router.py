from fastapi import APIRouter

from auth_app.api.endpoints import login, logout

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["tokens"])
api_router.include_router(logout.router, prefix="/logout", tags=["tokens"])
