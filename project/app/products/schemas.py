from decimal import Decimal

import requests
from pydantic import BaseModel, Field, PositiveInt, condecimal, conint, validator

from typing import Union, Optional
from scheduler import product_status_cache


class ProductSerializer(BaseModel):
    """
    Pydantic model to convert the sqlmodel stored in the database with
    some transformations in their attributes
    """

    name: str
    status_name: Optional[str]
    stock: PositiveInt
    description: str
    price: condecimal(ge=Decimal("0.0"), max_digits=10, decimal_places=2)
    discount: Optional[int]
    final_price: Optional[
        condecimal(ge=Decimal("0.0"), max_digits=10, decimal_places=2)
    ]
    product_id: int

    @validator("discount", always=True)
    def discount_fetch(cls, value, values):
        response = requests.get(
            url="https://www.randomnumberapi.com/api/v1.0/random?min=1&max=100"
        )
        assert response.status_code == 200, "Discount service is not working"
        discount_response = response.json().pop()

        values["discount"] = discount_response

        return discount_response

    @validator("final_price", always=True)
    def asd(cls, value, values):

        discount = Decimal((100 - values.get("discount")) / 100)
        temp = discount * values.get("price")
        return round(temp, 2)

    @validator("status_name", always=True)
    def status_name_cached(cls, value, values):
        product_id = values.get("product_id")
        if not (status := product_status_cache.get(product_id)):
            product_status_cache[product_id] = values.get("status")
            status = values.get("status")

        return "Active" if status else "Inactive"


class ModifyProduct(BaseModel):
    name: str
    status: Union[bool, None] = Field(default=True)
    stock: Union[conint(ge=0), None]
    description: Union[str, None]
    price: Union[condecimal(ge=Decimal("0.0"), max_digits=10, decimal_places=2), None]


class CreateProduct(BaseModel):
    name: str
    status: bool = Field(default=True)
    stock: conint(ge=0) = Field(default=0)
    description: str
    price: condecimal(ge=Decimal("0.0"), max_digits=10, decimal_places=2) = Field(
        default=0
    )
