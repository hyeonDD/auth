from typing import AsyncGenerator

from blog_app.db.mysql.session import mysql_session_factory


async def get_mysql_db() -> AsyncGenerator:
    async with mysql_session_factory() as db:
        yield db
