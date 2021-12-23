import json
from functools import lru_cache
from posixpath import join
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.schemas import Film, FilmShort


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 min


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic        
    
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        """Return film object."""             
        film = await self._film_from_cache(film_id)        
        if not film:            
            film = await self._get_film_from_elastic(film_id)
            if not film:                
                return None
            # Save film to cache
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        """Get film from ES"""
        doc = await self.elastic.get('movies', film_id)                
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        """Try to get film data from cache."""         
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def __films_list_from_cache(self, key: str) -> Optional[List[FilmShort]]:
        """Try to get films_list by query string from cache."""            
        films_list = await self.redis.get(key)        
        if not films_list:
            return None
        
        data = json.loads(films_list)
        films_list = []
        for film_short in data:
            films_list.append(FilmShort.parse_raw(film_short))        
        return films_list

    async def _put_film_to_cache(self, film: Film) -> None:
        """Save film data. Life time - 5 min. Pydantic dataclass `film` sereilze to json"""
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)
        
    async def _put_films_list_to_cache(self, key: str, films_list: List[FilmShort]) -> None:
        """Save films_list data. Key = query sting. Life time - 5 min."""
        print(key)
        data = []
        for film_short in films_list:
            data.append(film_short.json())
        data = json.dumps(data)
        await self.redis.set(key, data, expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    def __make_query(
        self,
        sort: Optional[str] = None,
        limit: Optional[str] = None,
        page: Optional[str] = None,
        filter_: Optional[str] = None,
        query: Optional[str] = None
    ) -> dict:
        """Make query for ES from query parameters."""
        query_obj = {'_source': [field for field in FilmShort.__fields__.keys()]}

        if sort:
            field = sort.split('-')  
            if '-' in sort:
                order = 'desc'
                field = sort.split('-')[-1]
            else: 
                order = 'asc'
                field = sort     
            field = 'title.raw' if field == 'title' else field            
            query_obj['sort'] = [{field: {'order': order}}]
        
        if filter_:
            query_obj['query'] = {'match': {'genre': filter_}}

        if query:
            query_obj['query'] = {'multi_match':{'query': f'{query}','fuzziness':'auto',
                    'fields': [
                        'actors_names',
                        'writers_names',
                        'title',
                        'description',
                        'genre'
                    ]}}
            
        query_obj['size'] = limit if limit else 10
        query_obj['from'] = int(page) * int(query_obj['size']) - int(query_obj['size']) if page else 1
        
        return query_obj

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
        query_ = self.__make_query(sort, limit, page, filter_, query)

        params = {sort, f"{limit}_limit", f"{page}_page", filter_, query}
        key = '_'.join(param for param in params if param)
                      
        films_list = await self.__films_list_from_cache(key)
        if not films_list:
            docs = await self.elastic.search(index='movies', body=query_)                          
            films_list = []
            for doc in docs['hits']['hits']:
                films_list.append(FilmShort(**doc['_source']))
        
            if films_list:        
                await self._put_films_list_to_cache(key, films_list)
        return films_list


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:    
    return FilmService(redis, elastic)
