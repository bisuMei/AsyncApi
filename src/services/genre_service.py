from functools import lru_cache
from typing import List, Optional

from aioredis import Redis

from db.elastic import get_elastic
from db.redis import get_redis

from elasticsearch import AsyncElasticsearch, exceptions

from fastapi import Depends, HTTPException

from models.schemas import GenreShort

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 min


class GenreService:

    def __init__(self, redis, elastic):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[GenreShort]:
        """Get genre info by id."""
        genre = await self._get_genre_from_elastic(genre_id)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[GenreShort]:
        try:
            doc = await self.elastic.get('genres', genre_id)
            return GenreShort(**doc['_source'])
        except exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")

    async def get_genres_list(self) -> List[GenreShort]:
        """Get list of genres. """
        docs = await self.elastic.search(index='genres')
        return [GenreShort(**doc['_source']) for doc in docs['hits']['hits']]


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
