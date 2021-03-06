from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends, HTTPException

from db.async_cache import AsyncCache
from db.async_search_engin import AsyncSearchEngin
from db.elastic import get_elastic
from db.redis import get_redis
from models.schemas import FilmShort, Person
from services.redis_service import RedisService
from services.elastic_service import ElasticSearchService, QueryParameters
from core.config import config


class PersonService:
    def __init__(self, redis, elastic):
        self.redis = redis
        self.elastic = elastic
        self._redis_service = RedisService(self.redis)
        self.elastic_service = ElasticSearchService(self.elastic)

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
            doc = await self.elastic_service.get(config.ELASTIC_INDEX['persons'], person_id)

            film_ids = doc['_source']['film_ids']
            films_query = self.elastic_service.films_query
            films_query['query']['ids']['values'] = film_ids

            key = f'films_by_person_{person_id}'
            films_list = await self._redis_service.get_models_list_from_cache(key, FilmShort)
            if not films_list:
                films_doc = await self.elastic_service.search(config.ELASTIC_INDEX['movies'], films_query)
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
        query_obj = {'_source': [field for field in Person.__fields__.keys()]}
        query_ = await self.elastic_service.make_person_query(
            query_obj=query_obj,
            query_params=QueryParameters(                
                limit=limit, 
                page=page,                 
                query=query
        ))
        print(query_)
            
        params = {f"{limit}_limit", f"{page}_page", query}
        key = 'persons_query_' + '_'.join(param for param in params if param)
        
        persons_list = await self._redis_service.get_models_list_from_cache(key, Person)
        if not persons_list:
            persons_doc = await self.elastic_service.search(config.ELASTIC_INDEX['persons'], query_)
            persons_list = [Person(**doc['_source']) for doc in persons_doc['hits']['hits']]

            if persons_list:
                await self._redis_service.put_models_list_to_cache(key, persons_list)
        return persons_list

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic_service.get(config.ELASTIC_INDEX['persons'], person_id)
            return Person(**doc['_source'])
        except exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")


@lru_cache()
def get_person_service(
        async_cache_storage: AsyncCache = Depends(get_redis),
        async_search_engin: AsyncSearchEngin = Depends(get_elastic),
) -> PersonService:
    return PersonService(async_cache_storage, async_search_engin)
