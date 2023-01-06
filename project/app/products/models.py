from typing import Optional, Annotated, Union
from pydantic.types import PositiveInt, conint
from sqlalchemy import UniqueConstraint, Column, String

from pydantic import condecimal
from sqlmodel import Field, SQLModel
from decimal import Decimal


class ProductBase(SQLModel):
    name: str = Field(sa_column_kwargs={"unique": True})
    status: bool = Field(default=True)
    stock: conint(ge=0) = Field(default=0)
    description: str
    price: condecimal(ge=Decimal("0.0"), max_digits=10, decimal_places=2) = Field(
        default=0
    )


class Product(ProductBase, table=True):
    product_id: int = Field(default=None, primary_key=True)
