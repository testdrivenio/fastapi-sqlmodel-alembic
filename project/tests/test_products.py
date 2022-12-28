import json


from http import HTTPStatus as status


from sqlalchemy import delete, select, insert
import logging

import pytest

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):


    yield


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}