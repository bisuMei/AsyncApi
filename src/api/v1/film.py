from typing import List, Optional
from fastapi import APIRouter

from models.schemas import Film, FilmShort
from services import film

from db.redis import get_redis
from db.elastic import get_elastic


router = APIRouter()


@router.get(
    '/{film_id}', 
    response_model=Film,
    summary='Film details',
    description='Film details with title, imdb_rating, description, persons, genres',
    response_description='Film with details by id'
)
async def film_details(film_id: str) -> Film:   
    redis = await get_redis() 
    elastic = await get_elastic()
    film_service = film.get_film_service(redis, elastic)     
    film_ = await film_service.get_by_id(film_id)
    return film_


@router.get(
    '/', 
    response_model=List[FilmShort],
    summary='Films list',
    description='Films list with id, title, imdb_rating. \
        Can be sorted by `imdb_ragin` and `title`. Pagination available. \
        `limit` - number of films per `page`. Can by filtered by ganre. \
        `query` - for serach by fields: actors_names, writers_names, title, description, genre',
    response_description='Films list with id, title, imdb_rating'
)
async def films(sort: Optional[str] = None,
                limit: Optional[str] = None,
                page: Optional[str] = None,
                filter_: Optional[str] = None,
                query: Optional[str] = None) -> List[FilmShort]:    
    redis = await get_redis() 
    elastic = await get_elastic()
    film_service = film.get_film_service(redis, elastic)     
    film_list = await film_service.get_films_list(sort, limit, page, filter_, query)
    return film_list

