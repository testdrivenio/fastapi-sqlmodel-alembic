from utils.base_class import AbstractRepository
from fastapi import HTTPException
from sqlalchemy import select, delete

from products.models import Product
from sqlmodel import SQLModel


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session, model):
        self.session = session
        self.model = model

    async def add(self, resource: SQLModel):
        new_resource = self.model(**resource.dict())
        self.session.add(new_resource)
        await self.session.commit()
        await self.session.refresh(new_resource)
        return new_resource

    async def get(self, resource_id: int):
        retrieved_resource = await self.session.get(self.model, resource_id)
        if not retrieved_resource:
            raise HTTPException(status_code=404, detail="Product not found")

        return retrieved_resource

    async def modify(self, resource_id: int, new_resource_content: SQLModel):

        product = await self.get(resource_id)
        values = new_resource_content.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(product, k, v)

        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

        return product

    async def delete(self, resource_id: int):


        retrieved_resource = await self.session.get(self.model, resource_id)
        if retrieved_resource:
            await self.session.delete(retrieved_resource)
            await self.session.commit()

        return None


    async def list_resource(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
