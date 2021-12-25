from typing import List, Optional

from fastapi import APIRouter
from fastapi.param_functions import Depends

from models.schemas import FilmShort, Person
from services.person_service import PersonService, get_person_service


router = APIRouter()


@router.get(
    '/{person_id}',
    response_model=Person,
    summary="Person details.",
    description="Person details with id, full_name, roles, films_ids",
    response_description="Person details by id.",
)
async def person_details(
    person_id: str,    
    person_service: PersonService = Depends(get_person_service)
) -> Person:
    return await person_service.get_by_id(person_id)


@router.get(
    '/{person_id}/film',
    response_model=List[FilmShort],
    summary='Film details by person.',
    description='Film details with title, imdb_rating, description, persons, genres',
    response_description='Film with details by person id.',
)
async def films_by_person(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> List[FilmShort]:        
    return await person_service.get_films_by_person(person_id)


@router.get(
    '/',
    response_model=List[Person],
    summary='Persons list details.',
    description='Get list of persons.',
    response_description='List of persons details with id, full_name, roles, films_ids',
)
async def persons(
        limit: Optional[str] = None,
        page: Optional[str] = None,
        query: Optional[str] = None,
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:        
    return await person_service.search_persons(limit, page, query)
