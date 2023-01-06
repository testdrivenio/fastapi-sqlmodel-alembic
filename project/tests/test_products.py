import logging

import pytest
from sqlalchemy import select, delete
from products.models import Product

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger(__name__)



def test_retrieve_products(test_app, session):
    """Test retrieve all products"""

    response = test_app.get(url="/products")

    result = session.execute(select(Product))

    assert response.status_code == 200
    for response_row, result_row in zip(response.json(), result.scalars().all()):
        result_row.price = float(result_row.price)
        assert response_row == result_row


def test_create_product(test_app, session):
    """Test create new product"""

    response = test_app.post(url="/products", json={
        "status": True,
        "stock": 88,
        "price": 6.42,
        "name": "LopaLOpa",
        "description": "deliver magnetic portals"
    })
    product_id = response.json().get('product_id')
    temp = session.get(Product, product_id)
    assert response.status_code == 202
    result = temp.dict()
    result = {**result, 'price': float(result.get('price'))}

    assert response.json() == result

    session.delete(temp)
    session.commit()


def test_modify_product(test_app, session):
    """Test modify product"""

    _ = test_app.post(url="/products", json={
        "status": True,
        "stock": 88,
        "price": 6.42,
        "name": "Dog dima don",
        "description": "deliver magnetic portals"
    })
    product_id = _.json().get('product_id')

    response_patch = test_app.patch(url=f"/products/{product_id}", json={
        "status": False,
        "name": "DracuKeooOzzz",
    })
    temp = {
        "status": False,
        "stock": 88,
        "price": 6.42,
        "name": "DracuKeooOzzz",
        "description": "deliver magnetic portals"
    }
    assert response_patch.status_code == 202
    assert response_patch.json() == temp

    session.delete(temp)
    session.commit()


def test_delete_product(test_app, session):
    """Test delete product"""

    _ = test_app.post(url="/products", json={
        "status": True,
        "stock": 88,
        "price": 6.42,
        "name": "Dog dima don",
        "description": "deliver magnetic portals"
    })
    product_id = _.json().get('product_id')

    response_delete = test_app.delete(url=f"/products/{product_id}")

    assert response_delete.status_code == 202

    response_get = test_app.get(url=f"/products/{product_id}")
    assert response_get.status_code == 404


def test_create_duplicate_products(test_app, session):
    """Test product name uniqueness"""

    _ = test_app.post(url="/products", json={
        "status": True,
        "stock": 88,
        "price": 6.42,
        "name": "Dog dima don",
        "description": "deliver magnetic portals"
    })
    product_id = _.json().get('product_id')
    response = test_app.post(url="/products", json={
        "status": True,
        "stock": 88,
        "price": 6.42,
        "name": "Dog dima don",
        "description": "deliver magnetic portals"
    })

    assert response.status_code == 409
    temp = session.get(Product, product_id)
    session.delete(temp)
    session.commit()


@pytest.mark.parametrize(
    "body_request,error_message",
    [
        (
                {
                    "status": True,
                    "stock": 88,
                    "price": -12,
                    "name": "Dog dima don",
                    "description": "deliver magnetic portals"
                },
                {
                    "loc": [
                        "body",
                        "price"
                    ],
                    "msg": "ensure this value is greater than or equal to 0.0",
                    "type": "value_error.number.not_ge",
                    "ctx": {
                        "limit_value": 0
                    }
                }

        ),
        (
                {

                    "status": True,
                    "stock": -88,
                    "price": 12,
                    "name": "Dog dima don",
                    "description": "deliver magnetic portals"
                },
                {
                    "loc": [
                        "body",
                        "stock"
                    ],
                    "msg": "ensure this value is greater than or equal to 0",
                    "type": "value_error.number.not_ge",
                    "ctx": {
                        "limit_value": 0
                    }
                }

        )
    ],
)
def test_product_validation(test_app, session, body_request, error_message):
    """Test body request validation"""

    response = test_app.post(url="/products", json=body_request)

    assert response.status_code == 422
    details = response.json().get("detail").pop()

    assert details.get("msg") == error_message.get("msg")
    assert details.get("type") == error_message.get("type")
    assert details.get("loc") == error_message.get("loc")
