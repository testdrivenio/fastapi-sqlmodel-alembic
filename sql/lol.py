import csv
import os
from dataclasses import Field
from functools import reduce, partial
from typing import Optional, Callable, List

import requests
from pydantic import PositiveInt, BaseModel, condecimal, validator, root_validator
from decimal import Decimal
from sqlalchemy import select
# from sqlmodel import create_engine, Session

from products.models import Product

a = {}


class ProductSerializer(BaseModel):
    """
        Pydantic model to convert the sqlmodel stored in the database with
        some transformations in their attributes
    """
    name: str
    status_name: Optional[str]
    stock: PositiveInt
    description: str
    price: condecimal(ge=Decimal('0.0'), max_digits=10, decimal_places=2)
    discount: Optional[int]
    final_price: Optional[condecimal(ge=Decimal('0.0'), max_digits=10, decimal_places=2)]
    product_id: int

    @validator('discount', always=True)
    def discount_fetch(cls, value, values):
        response = requests.get(url="https://www.randomnumberapi.com/api/v1.0/random?min=1&max=100")
        assert response.status_code == 200, "Discount service is not working"
        discount_response = response.json().pop()

        values['discount'] = discount_response

        return discount_response

    @validator('final_price', always=True)
    def asd(cls, value, values):

        discount = Decimal((100 - values.get('discount')) / 100)
        temp = discount * values.get('price')
        return round(temp, 2)

    @validator('status_name', always=True)
    def status_name_cached(cls, value, values):
        product_id = values.get('product_id')
        if not (status := product_status_cache.get(product_id)):
            product_status_cache[product_id] = values.get('status')
            status = values.get('status')

        return "Active" if status else "Inactive"

product_status_cache = {}


def status_name_cached(values: dict):
    product_id = values.get('product_id')
    if not (status := product_status_cache.get(product_id)):
        product_status_cache[product_id] = values.get('status')
        status = values.get('status')

    return {
        **values,
        'status_name': status
    }


def final_price_applier(values: dict):
    response = requests.get(url="https://www.randomnumberapi.com/api/v1.0/random?min=1&max=100")
    assert response.status_code == 200, "Discount service is not working"
    discount_response = response.json().pop()
    discount = (100 - discount_response) / 100
    return {**values,
            'final_price': Decimal(values.get('price') * discount),
            'discount': discount_response
            }


def transform_response(*functions_appliers: List[Callable], data: dict = {}) -> dict:
    return reduce((lambda d, func: func(d)), functions_appliers, data)


product_serializer = partial(transform_response, final_price_applier, status_name_cached)

a = {
    "status": False,
    "stock": 88,
    "price": 6.42,
    "product_id": 1,
    "name": "Quiche Assorted",
    "description": "deliver magnetic portals"
}
print(ProductSerializer(**a))

exit()
