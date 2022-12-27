from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.products.models import Product
from fastapi import APIRouter

product_router = APIRouter()

@product_router.get("/products", response_model=list[Product])
async def get_product(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product))
    songs = result.scalars().all()
    return [song for song in songs]


@product_router.post("/products", response_model=list[Product])
async def post_product(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product))
    songs = result.scalars().all()
    return [song.dict() for song in songs]

"""
@router.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
"""