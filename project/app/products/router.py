from fastapi import Depends, FastAPI, Body

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status as http_status
from app.db import get_session
from app.products.models import Product, ProductBase, ProductCreate
from fastapi import APIRouter
from app.products.service import SqlAlchemyRepository

product_router = APIRouter()


@product_router.get("/", response_model=list[Product], status_code=http_status.HTTP_200_OK)
async def list_products(session: AsyncSession = Depends(get_session)):
    crud_instance = SqlAlchemyRepository(session, Product)
    result = await crud_instance.list_resource()
    return result


@product_router.get("/{product_id}", response_model=Product, status_code=http_status.HTTP_200_OK)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    crud_instance = SqlAlchemyRepository(session, Product)
    retrieved_resource = await crud_instance.get(product_id)
    return retrieved_resource


@product_router.post("/", response_model=Product, status_code=http_status.HTTP_202_ACCEPTED)
async def post_product(product_body: ProductBase, session: AsyncSession = Depends(get_session)):
    crud_instance = SqlAlchemyRepository(session, Product)
    result: Product = await crud_instance.add(product_body)

    return result


@product_router.put("/{product_id}", response_model=Product, status_code=http_status.HTTP_202_ACCEPTED)
async def put_product(product_id: int, product_body: ProductBase, session: AsyncSession = Depends(get_session)):
    crud_instance = SqlAlchemyRepository(session, Product)
    result: Product = await crud_instance.update(product_id, product_body)
    return result


@product_router.patch("/{product_id}", response_model=Product, status_code=http_status.HTTP_202_ACCEPTED)
async def patch_product(product_id: int, product_body: ProductBase, session: AsyncSession = Depends(get_session)):
    crud_instance = SqlAlchemyRepository(session, Product)
    result: Product = await crud_instance.update(product_id, product_body)
    return result


@product_router.delete("/{product_id}", status_code=http_status.HTTP_202_ACCEPTED)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    crud_instance = SqlAlchemyRepository(session, Product)
    result: Product = await crud_instance.delete(product_id)
    return {}
