from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.products.router import product_router

app = FastAPI()

app.include_router(product_router, prefix="/product")


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
