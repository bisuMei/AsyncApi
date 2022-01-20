from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends, HTTPException

from db.elastic import get_elastic
from db.redis import get_redis
from models.schemas import Film, FilmShort
from services.redis_service import RedisService
from services.elastic_service import ElasticSearchService, QueryParameters
from core import config


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self._redis_service = RedisService(self.redis)
        self.elastic_service = ElasticSearchService(self.elastic)

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        """Return film object."""
        key = f"{FilmService.__name__}__movies_index__{film_id}"
        film = await self._redis_service.get_model_from_cache(film_id, Film)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            # Save film to cache                                   
            await self._redis_service.put_model_to_cache(key, film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        """Get film from ES"""
        try:
            doc = await self.elastic_service.get(config.ELASTIC_INDEX['movies'], film_id)
            return Film(**doc['_source'])
        except exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")

    async def get_films_list(
            self,
            sort: Optional[str] = None,
            limit: Optional[str] = None,
            page: Optional[str] = None,
            filter_: Optional[str] = None,
            query: Optional[str] = None,
    ) -> List[FilmShort]:
        """Get films with query parameters. 
        `sort` - sorting by field.
        `limit` - count of records per page
        `page` - page number
        `filter_` - filtered records by genre
        `query` - query for search on next fields: actors_names, writers_names,
            title, description, genre
        """
        query_obj = {'_source': [field for field in FilmShort.__fields__.keys()]}
        
        query_ = await self.elastic_service.make_query(
            query_obj=query_obj, 
            query_params=QueryParameters(
                sort=sort, 
                limit=limit, 
                page=page, 
                filter_=filter_, 
                query=query
        ))
        
        params = {sort, f"{limit}_limit", f"{page}_page", filter_, query}
        key = '_'.join(param for param in params if param)

        films_list = await self._redis_service.get_models_list_from_cache(key, FilmShort)
        if not films_list:            
            docs = await self.elastic_service.search(config.ELASTIC_INDEX['movies'], query_)
            films_list = []
            for doc in docs['hits']['hits']:
                films_list.append(FilmShort(**doc['_source']))

            if films_list:
                await self._redis_service.put_models_list_to_cache(key, films_list)
        return films_list


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
