from fastapi import APIRouter
from sqlalchemy import insert

from register_app.db.mysql.base_class import Base
from register_app.db.mysql.session import engine
from register_app.models.mysql.user import User
from register_app.core.security import get_password_hash

router = APIRouter()


@router.post("/", status_code=201)
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(insert(User).values(nickname='superuser', email='superuser@example.com', password=get_password_hash('1'), permission='superuser'))
    return {"message": "Table and Colum Create Successful"}


@router.delete("/", status_code=200)
async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    return {"message": "Table and Colum Delete Successful"}
