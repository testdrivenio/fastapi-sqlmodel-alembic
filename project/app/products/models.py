from typing import Optional, Annotated
from pydantic.types import PositiveInt

from pydantic import condecimal
from sqlmodel import Field, SQLModel
from decimal import Decimal


class ProductBase(SQLModel):
    name: str
    status: bool = Field(default=True)
    stock: PositiveInt = Field(default=0)
    description: str
    price: condecimal(ge=Decimal('0.0'), max_digits=10, decimal_places=2) = Field(default=0)


class Product(ProductBase, table=True):
    product_id: int = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass
