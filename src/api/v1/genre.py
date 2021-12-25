from typing import List, Optional

from fastapi import APIRouter
from fastapi.param_functions import Depends

from db.elastic import get_elastic, AsyncElasticsearch
from db.redis import get_redis, Redis

from models.schemas import GenreShort
from services.genre_service import get_genre_service, GenreService


router = APIRouter()


@router.get(
    '/{genre_id}',
    response_model=GenreShort,
    summary='Genre details',
    description='Genres details with id, name.',
    response_description='Genres details by id.',
)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> Optional[GenreShort]:        
    return await genre_service.get_by_id(genre_id)


@router.get(
    '/',
    response_model=List[GenreShort],
    summary='Genres list.',
    description="Genres list with id, name.",
    response_description="Genres list"
)
async def genres_list(
    genre_service: GenreService = Depends(get_genre_service)
) -> List[GenreShort]:
    return await genre_service.get_genres_list()
