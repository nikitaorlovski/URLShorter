from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from models.url_model import Base

from .config import settings

engine = create_async_engine(settings.DB_URL, pool_pre_ping=True)

new_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with new_session() as session:
        yield session


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
