from register_app.core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

# echo bool 값에 따라 실행하는 쿼리 확인 가능
engine = create_async_engine(settings.MYSQL_URL, echo=True)

# expire_on_commit bool 값으로 커밋후 객체 만료 설정 가능
mysql_session_factory = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)
