import json
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends, HTTPException

from db.elastic import get_elastic
from db.redis import get_redis
from models.schemas import FilmShort, Person
from services.redis_service import RedisService


class PersonService:
    person_query = {
            "match": {
                "full_name": {
                    "query": "{name}",
                    "fuzziness": "AUTO"
                }
            }
        }

    films_query = {
        '_source': ['id', 'title', 'imdb_rating'],
        'query': {
            'ids': {
                'values': []
            }
        }
    }

    def __init__(self, redis, elastic):
        self.redis = redis
        self.elastic = elastic
        self._redis_service = RedisService(self.redis)

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        """Return person info by id."""
        key = f"{PersonService.__name__}__persons_index__{person_id}"
        person = await self._redis_service.get_model_from_cache(key, Person)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None            
            await self._redis_service.put_model_to_cache(key, person)
        return person
 
    async def get_films_by_person(self, person_id: str) -> List[FilmShort]:
        """Return films by related person."""
        try:
            doc = await self.elastic.get('persons', person_id)
            film_ids = doc['_source']['film_ids']              
            self.films_query['query']['ids']['values'] = film_ids            
            key = f'films_by_person_{person_id}'
            films_list = await self._redis_service.get_models_list_from_cache(key, FilmShort)
            if not films_list:
                print('-'*100)
                print(self.films_query)
                films_doc = await self.elastic.search(index='movies', body=self.films_query)                
                films_list = []
                for doc in films_doc['hits']['hits']:
                    films_list.append(FilmShort(**doc['_source']))

                if films_list:
                    await self._redis_service.put_models_list_to_cache(key, films_list)
            return films_list
        except exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")

    async def search_persons(
            self,
            limit: Optional[str] = None,
            page: Optional[str] = None,
            query: Optional[str] = None,
    ) -> List[Person]:
        """Return persons by query params."""
        query_ = self._make_search_query(limit, page, query)
        params = {f"{limit}_limit", f"{page}_page", query}
        key = 'persons_query_' + '_'.join(param for param in params if param)
        
        persons_list = await self._redis_service.get_models_list_from_cache(key, Person)
        if not persons_list:
            persons_doc = await self.elastic.search(index='persons', body=query_)
            persons_list = [Person(**doc['_source']) for doc in persons_doc['hits']['hits']]

            if persons_list:
                await self._redis_service.put_models_list_to_cache(key, persons_list)
        return persons_list

    def _make_search_query(
        self,
        limit: Optional[str] = None,
        page: Optional[str] = None,
        query: Optional[str] = None,
    ) -> dict:
        query_obj = {'_source': [field for field in Person.__fields__.keys()]}
        if query:
            self.person_query['match']['full_name']['query'] = query
            query_obj['query'] = self.person_query
        query_obj['size'] = limit if limit else 10
        query_obj['from'] = int(page) * int(query_obj['size']) - int(query_obj['size']) if page else 1

        return query_obj

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get('persons', person_id)
            return Person(**doc['_source'])
        except exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
