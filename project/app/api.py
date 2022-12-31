import asyncio
import logging

from pathlib import Path

from fastapi import Depends, FastAPI
from utils.custom_logger import CustomizeLogger
from products.router import product_router

logger = logging.getLogger(__name__)

config_path = Path(__file__).with_name("logging_config.json")


def create_app() -> FastAPI:
    new_app = FastAPI(title='Products API', debug=False)
    new_app.logger = CustomizeLogger.make_logger(config_path)

    return new_app


app = create_app()
app.include_router(product_router, prefix="/product")
