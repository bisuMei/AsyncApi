from typing import List, Optional
from fastapi import APIRouter

from models.schemas import Film, FilmShort
from services import film

from db.redis import get_redis
from db.elastic import get_elastic


router = APIRouter()


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str) -> Film:   
    redis = await get_redis() 
    elastic = await get_elastic()
    film_service = film.get_film_service(redis, elastic)     
    film_ = await film_service.get_by_id(film_id)
    return film_


@router.get('/', response_model=List[FilmShort])
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

