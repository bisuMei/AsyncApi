from typing import List, Optional

from db.elastic import get_elastic
from db.redis import get_redis

from fastapi import APIRouter

from models.schemas import GenreShort
from services.genre_service import get_genre_service

router = APIRouter()


@router.get('/{genre_id}', response_model=GenreShort)
async def genre_details(genre_id: str) -> Optional[GenreShort]:
    redis = await get_redis()
    elastic = await get_elastic()
    genre_service = get_genre_service(redis, elastic)
    genre_info = await genre_service.get_by_id(genre_id)
    return genre_info


@router.get('/', response_model=List[GenreShort])
async def genres_list() -> List[GenreShort]:
    redis = await get_redis()
    elastic = await get_elastic()
    genre_service = get_genre_service(redis, elastic)
    genres_list = await genre_service.get_genres_list()
    return genres_list
