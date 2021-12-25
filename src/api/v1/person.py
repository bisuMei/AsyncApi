from typing import List, Optional

from fastapi import APIRouter
from fastapi.param_functions import Depends

from db.elastic import get_elastic, AsyncElasticsearch
from db.redis import get_redis, Redis

from models.schemas import FilmShort, Person
from services.person_service import get_person_service


router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(
    person_id: str,
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> Person:
    person_service = get_person_service(redis, elastic)
    person_info = await person_service.get_by_id(person_id)
    return person_info


@router.get('/{person_id}/film', response_model=List[FilmShort])
async def films_by_person(
    person_id: str,
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> List[FilmShort]:
    person_service = get_person_service(redis, elastic)
    person_films_list = await person_service.get_films_by_person(person_id)
    return person_films_list


@router.get('/', response_model=List[Person])
async def persons(
        limit: Optional[str] = None,
        page: Optional[str] = None,
        query: Optional[str] = None,
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
):
    person_service = get_person_service(redis, elastic)
    persons = await person_service.search_persons(limit, page, query)
    return persons
