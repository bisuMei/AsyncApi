from typing import List, Optional
from fastapi import APIRouter
from fastapi.param_functions import Depends

from models.schemas import Film, FilmShort
from services import film
from services.auth_handler import JWTBearer, get_permissions
from utils.constants import ACTION
from utils.decorators import auth_required

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=Film,
    summary='Film details',
    description='Film details with title, imdb_rating, description, persons, genres',
    response_description='Film with details by id',
    dependencies=[Depends(JWTBearer())],
)
@auth_required(ACTION.film_by_id)
async def film_details(
    film_id: str,
    film_service: film.FilmService = Depends(film.get_film_service),
    token: str = Depends(JWTBearer()),
) -> Film:
    return await film_service.get_by_id(film_id)


@router.get(
    '/',
    response_model=List[FilmShort],
    summary='Films list',
    description='Films list with id, title, imdb_rating. \
        Can be sorted by `imdb_rating` and `title`. Pagination available. \
        `limit` - number of films per `page` (10 by default). \
        `filter_` - Can by filtered by ganre. \
        `query` - for serach by fields: actors_names, writers_names, title, description, genre',
    response_description='Films list with id, title, imdb_rating',
    dependencies=[Depends(JWTBearer())],
)
@auth_required(ACTION.films)
async def films(
    film_service: film.FilmService = Depends(film.get_film_service),
    token: str = Depends(JWTBearer()),
    sort: Optional[str] = None,
    limit: Optional[str] = None,
    page: Optional[str] = None,
    filter_: Optional[str] = None,
    query: Optional[str] = None
) -> List[FilmShort]:
    return await film_service.get_films_list(sort, limit, page, filter_, query)
