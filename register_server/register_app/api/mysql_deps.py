from typing import AsyncGenerator

from register_app.db.mysql.session import mysql_session_factory


async def get_db() -> AsyncGenerator:
    async with mysql_session_factory() as db:
        yield db
