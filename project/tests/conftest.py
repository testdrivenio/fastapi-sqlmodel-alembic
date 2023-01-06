import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from api import app


@pytest.fixture(scope="session")
def test_app():
    with TestClient(app) as ac:
        yield ac


@pytest.fixture(scope="session")
def session():

    engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/dev")
    with Session(engine) as session:
        yield session
