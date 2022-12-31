from decimal import Decimal

from pydantic import BaseModel, ValidationError, validator, Field, PositiveInt, condecimal
from fastapi import Body, FastAPI
from typing import Union


class ProductSerializer(BaseModel):
    name: str
    status_name: str
    stock: PositiveInt = Field(default=0)
    description: str
    price: condecimal(ge=Decimal('0.0'), max_digits=10, decimal_places=2) = Field(default=0)
    discount: int
    final_price: condecimal(ge=Decimal('0.0'), max_digits=10, decimal_places=2) = Field(default=0)



    @validator('status_name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        # https://www.randomnumberapi.com/api/v1.0/random?min=100&max=1000
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v





