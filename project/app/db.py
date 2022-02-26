from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from app.settings import Settings

settings = Settings()

print('settings.ASYNC_DATABASE_URI', settings.ASYNC_DATABASE_URI)
engine = AsyncEngine(create_engine(settings.ASYNC_DATABASE_URI, echo=True, future=True))

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
