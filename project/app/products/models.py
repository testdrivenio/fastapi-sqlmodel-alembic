from typing import Optional

from pydantic.types import conint

from pydantic import condecimal
from sqlmodel import Field, SQLModel
from decimal import Decimal


class ProductBase(SQLModel):
    name: Optional[str]
    status: Optional[bool]
    stock: Optional[conint(ge=0)]
    description: Optional[str]
    price: Optional[condecimal(ge=Decimal("0.0"), max_digits=10, decimal_places=2)]


class Product(ProductBase, table=True):
    product_id: int = Field(default=None, primary_key=True)
