from fastapi import Depends

from fastapi import status as http_status
from db import get_sqlalchemy_crud
from products.models import Product, ProductBase
from products.schemas import ModifyProduct, CreateProduct
from fastapi import APIRouter
from products.service import ProductORM
from functools import partial


product_router = APIRouter()
product_crud = partial(get_sqlalchemy_crud, ProductORM)

@product_router.get("/", response_model=list[Product], status_code=http_status.HTTP_200_OK)
async def list_products(crud_instance: ProductORM = Depends(product_crud)):

    result = await crud_instance.list_resource()
    return result


@product_router.get("/{product_id}", response_model=Product, status_code=http_status.HTTP_200_OK)
async def get_product(product_id: int,
                      crud_instance: ProductORM = Depends(product_crud)):

    retrieved_resource = await crud_instance.get(product_id)
    return retrieved_resource


@product_router.post("/", response_model=Product, status_code=http_status.HTTP_202_ACCEPTED)
async def post_product(product_body: CreateProduct,
                       crud_instance: ProductORM = Depends(product_crud)):
    result = await crud_instance.add(product_body.dict())
    return result


@product_router.put("/{product_id}", status_code=http_status.HTTP_202_ACCEPTED)
async def put_product(product_id: int, product_body: ModifyProduct, crud_instance: ProductORM = Depends(product_crud)):

    await crud_instance.modify(product_id, product_body.dict())
    return {}


@product_router.patch("/{product_id}", status_code=http_status.HTTP_202_ACCEPTED)
async def patch_product(product_id: int,
                        product_body: ProductBase,
                        crud_instance: ProductORM = Depends(product_crud)):

    await crud_instance.modify(product_id, product_body.dict())
    return {}


@product_router.delete("/{product_id}", status_code=http_status.HTTP_202_ACCEPTED)
async def delete_product(product_id: int, crud_instance: ProductORM = Depends(product_crud)):
    await crud_instance.delete(product_id)
    return {}
