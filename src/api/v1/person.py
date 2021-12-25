from typing import List, Optional

from fastapi import APIRouter
from fastapi.param_functions import Depends

from db.elastic import get_elastic, AsyncElasticsearch
from db.redis import get_redis, Redis

from models.schemas import FilmShort, Person
from services.person_service import PersonService, get_person_service, Person


router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(
    person_id: str,    
    person_service: PersonService = Depends(get_person_service)
) -> Person:
    return await person_service.get_by_id(person_id)


@router.get('/{person_id}/film', response_model=List[FilmShort])
async def films_by_person(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> List[FilmShort]:        
    return await person_service.get_films_by_person(person_id)


@router.get('/', response_model=List[Person])
async def persons(
        limit: Optional[str] = None,
        page: Optional[str] = None,
        query: Optional[str] = None,
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:        
    return await person_service.search_persons(limit, page, query)
