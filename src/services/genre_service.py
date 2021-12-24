import json
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends, HTTPException

from db.elastic import get_elastic
from db.redis import get_redis
from models.schemas import Genre, GenreShort
from services.redis_service import RedisService


class GenreService:

    def __init__(self, redis, elastic):
        self.redis = redis
        self.elastic = elastic
        self._redis_service = RedisService(self.redis)    
    
    async def get_by_id(self, genre_id: str) -> Optional[GenreShort]:
        """Get genre info by id."""
        key = f"{GenreService.__name__}__genres_index__{genre_id}"
        genre = await self._redis_service.get_model_from_cache(genre_id, Genre)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None            
            await self._redis_service.put_model_to_cache(key, genre)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[GenreShort]:
        try:
            doc = await self.elastic.get('genres', genre_id)
            return GenreShort(**doc['_source'])
        except exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")

    async def get_genres_list(self) -> List[GenreShort]:
        """Get list of genres. """
        genres_list = await self._redis_service.get_models_list_from_cache('genre', Genre)
        if not genres_list:
            docs = await self.elastic.search(index='genres')
            genres_list = [GenreShort(**doc['_source']) for doc in docs['hits']['hits']]

            if genres_list:
                await self._redis_service.put_models_list_to_cache('genres', genres_list)

        return genres_list


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
