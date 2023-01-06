import os
from typing import Type


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from utils.base_class import AbstractRepository

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, future=True)


async def get_sqlalchemy_crud(
    crud_class: Type[AbstractRepository],
) -> Type[AbstractRepository]:
    """
    Creates a version asynchronous session of sqlalchemy
    """
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        temp = crud_class(session)
        yield temp
