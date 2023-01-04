import logging

import pytest
from sqlalchemy import select
import pytest_asyncio
from db import get_sqlalchemy_crud
from products.models import Product
from products.service import ProductORM

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):

    yield
    retrieved_resource = await self.session.get(Product, resource_id)
    if retrieved_resource:
        await self.session.delete(retrieved_resource)
        await self.session.commit()

@pytest.mark.asyncio
async def test_retrieve_products(test_app, session):
    response = test_app.get("/products")

    result = await session.execute(select(Product))
    assert response.status_code == 200
    assert response.json() == result.scalars().all()


@pytest.mark.asyncio
async def test_retrieve_products(test_app, session):
    response = test_app.post("/products", json={})

    result = await session.execute(select(Product))
    assert response.status_code == 200
    assert response.json() == result.scalars().all()