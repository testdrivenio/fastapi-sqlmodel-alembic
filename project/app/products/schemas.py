from decimal import Decimal

from pydantic import BaseModel, ValidationError, validator, Field, PositiveInt, condecimal, conint
from fastapi import Body, FastAPI
from typing import Union


class ProductSerializer(BaseModel):
    """
        Pydantic model to convert the sqlmodel stored in the database with
        some transformations in their attributes
    """
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

    @validator('discount')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        # https://www.randomnumberapi.com/api/v1.0/random?min=100&max=1000
        return v

    @validator('final_price')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


class ModifyProduct(BaseModel):
    name: str
    status: Union[bool, None] = Field(default=True)
    stock: Union[conint(ge=0), None]
    description: Union[str, None]
    price: Union[condecimal(ge=Decimal('0.0'), max_digits=10, decimal_places=2), None]


class CreateProduct(BaseModel):
    name: str
    status: bool = Field(default=True)
    stock: conint(ge=0) = Field(default=0)
    description: str
    price: condecimal(ge=Decimal('0.0'), max_digits=10, decimal_places=2) = Field(default=0)
