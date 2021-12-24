import json
from typing import Optional, List, Union

from models.schemas import Film, FilmShort, Genre, GenreShort, Person, GenreShort


CACHE_EXPIRE_IN_SECONDS = 60 * 5 # 5 min by default


class RedisService:

    def __init__(self, redis, expire: int = CACHE_EXPIRE_IN_SECONDS) -> None:
        self.__redis = redis
        self.__expire = expire 

    async def put_model_to_cache(self, key: str, model: Union[Film, Genre, Person]) -> None:
        await self.__redis.set(key, model.json(), expire=self.__expire)

    async def get_model_from_cache(self, key: str, model: Union[Film, Genre, Person]) -> Optional[Union[Film, Genre, Person]]:                 
        data = await self.__redis.get(key)
        if not data:
            return None
        return model.parse_raw(data)

    async def get_models_list_from_cache(
        self, 
        redis_key: str, 
        model: Union[FilmShort, Genre, Person]
    ) -> Optional[List[Union[FilmShort, Genre, Person]]]:
        """Try to get films_list by query string from cache."""            
        models_list = await self.__redis.get(redis_key)        
        if not models_list:
            return None        
        data = json.loads(models_list)
        models_list = []
        for item in data:
            models_list.append(model.parse_raw(item))        
        return models_list

    async def put_models_list_to_cache(
        self, 
        redis_key: str, 
        models_list: List[Union[FilmShort, Genre, Person]]) -> None:
        """Save films_list data. Key = query sting. Life time - 5 min."""
        data = []
        for model in models_list:
            data.append(model.json())
        data = json.dumps(data)
        await self.__redis.set(redis_key, data, expire=self.__expire)