from fastapi import APIRouter

from blog_app.api.endpoints import users, init_db

api_router = APIRouter()
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(init_db.router, prefix="/init-db", tags=["init"])
