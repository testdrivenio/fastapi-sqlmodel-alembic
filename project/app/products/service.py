from sqlalchemy.exc import IntegrityError

from utils.base_class import AbstractRepository
from fastapi import HTTPException
from sqlalchemy import select, delete, update

from products.models import Product


class ProductORM(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, resource: dict) -> dict:

        new_resource = Product(**resource)
        try:
            self.session.add(new_resource)
            await self.session.commit()
            await self.session.refresh(new_resource)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Product name is already taken")

        return new_resource.dict()

    async def get(self, resource_id: int):
        retrieved_resource = await self.session.get(Product, resource_id)
        if not retrieved_resource:
            raise HTTPException(status_code=404, detail="Product not found")

        return retrieved_resource

    async def modify(self, resource_id: int, new_resource_content: dict):

        await self.get(resource_id)

        stmt = (
            update(Product)
            .where(Product.product_id == resource_id)
            .values(new_resource_content)
        )

        await self.session.execute(stmt)
        await self.session.commit()
        return None

    async def delete(self, resource_id: int):

        retrieved_resource = await self.session.get(Product, resource_id)
        if not retrieved_resource:
            raise HTTPException(status_code=404, detail="Product not found")

        await self.session.delete(retrieved_resource)
        await self.session.commit()

        return None

    async def list_resource(self):
        result = await self.session.execute(select(Product).limit(10))
        return result.scalars().all()
