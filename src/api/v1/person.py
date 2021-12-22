from typing import List, Optional

from db.elastic import get_elastic
from db.redis import get_redis

from fastapi import APIRouter

from models.schemas import FilmShort, Person
from services.person_service import get_person_service

router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str) -> Person:
    redis = await get_redis()
    elastic = await get_elastic()
    person_service = get_person_service(redis, elastic)
    person_info = await person_service.get_by_id(person_id)
    return person_info


@router.get('/{person_id}/film', response_model=List[FilmShort])
async def films_by_person(person_id: str) -> List[FilmShort]:
    redis = await get_redis()
    elastic = await get_elastic()
    person_service = get_person_service(redis, elastic)
    person_films_list = await person_service.get_films_by_person(person_id)
    return person_films_list


@router.get('/', response_model=List[Person])
async def persons(
        limit: Optional[str] = None,
        page: Optional[str] = None,
        query: Optional[str] = None,
):
    redis = await get_redis()
    elastic = await get_elastic()
    person_service = get_person_service(redis, elastic)
    persons = await person_service.search_persons(limit, page, query)
    return persons
