import asyncio
import os
from typing import Type

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from starlette.testclient import TestClient

from api import app

@pytest.fixture
def test_app():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(
        os.environ.get("DATABASE_URL")
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def session(engine):
    async with AsyncSession(engine) as async_session:
        yield async_session

