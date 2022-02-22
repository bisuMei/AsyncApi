from typing import List, Optional

from fastapi import APIRouter
from fastapi.param_functions import Depends

from models.schemas import GenreShort
from services.auth_handler import get_permissions, JWTBearer
from services.genre_service import get_genre_service, GenreService
from utils.constants import ACTION
from utils.decorators import auth_required

router = APIRouter()


@router.get(
    '/{genre_id}',
    response_model=GenreShort,
    summary='Genre details',
    description='Genres details with id, name.',
    response_description='Genres details by id.',
    dependencies=[Depends(JWTBearer())],
)
@auth_required(ACTION.genre_by_id)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
    token: str = Depends(JWTBearer()),
) -> Optional[GenreShort]:
    if await get_permissions(ACTION.genre_by_id, token):
        return await genre_service.get_by_id(genre_id)


@router.get(
    '/',
    response_model=List[GenreShort],
    summary='Genres list.',
    description="Genres list with id, name.",
    response_description="Genres list",
    dependencies=[Depends(JWTBearer())],
)
@auth_required(ACTION.genres)
async def genres_list(
    genre_service: GenreService = Depends(get_genre_service),
    token: str = Depends(JWTBearer()),
) -> List[GenreShort]:
    if await get_permissions(ACTION.genres, token):
        return await genre_service.get_genres_list()
