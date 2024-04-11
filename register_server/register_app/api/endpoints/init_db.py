from register_app.db.mysql.base_class import Base
from register_app.db.mysql.session import engine

from fastapi import APIRouter


router = APIRouter()


@router.post("/", status_code=201)
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return {"message": "Table and Colum Create Successful"}


@router.delete("/", status_code=200)
async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    return {"message": "Table and Colum Delete Successful"}
