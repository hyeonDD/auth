from fastapi import APIRouter, Depends

from blog_app.db.mysql.base_class import Base
from blog_app.db.mysql.session import engine
from blog_app.api.authorization_deps import is_superuser


router = APIRouter(dependencies=[Depends(is_superuser)])


@router.post("/", status_code=201)
async def create_tables() -> dict:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "User DB Table and Colum, Redis Cache Create Successful"}


@router.delete("/", status_code=200)
async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    return {"message": "User DB Table and Colum, Redis Cache Delete Successful"}
