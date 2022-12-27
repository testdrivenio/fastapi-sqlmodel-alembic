from typing import Optional, Annotated
from pydantic.types import PositiveInt

from pydantic import condecimal
from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str
    status: bool = Field(default=True)
    stock: PositiveInt = Field(default=0)
    description: str
    price: condecimal(max_digits=10, decimal_places=2) = Field(default=0)

class Product(ProductBase, table=True):
    product_id: int = Field(default=None, primary_key=True)