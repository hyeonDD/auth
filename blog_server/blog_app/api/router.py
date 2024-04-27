from fastapi import APIRouter

from blog_app.api.endpoints import init_db
from blog_app.api.endpoints import posts

api_router = APIRouter()
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(init_db.router, prefix="/init-db", tags=["init"])
