import orjson

from pydantic import BaseModel
from typing import List, Optional


def orjson_dumps(v, *, default):
    """`orjson.dumps` returns bytes, pydantic needed unicode."""
    return orjson.dumps(v, default=default).decode()


class InstanceSchema(BaseModel):
    id: str
    name: str


class BaseFields(BaseModel):
    class Config:
        fields = {'field_value': 'fields'}


class FilmShort(BaseFields):
    id: str
    title: str
    imdb_rating: Optional[float]

    
class GenreShort(BaseFields):
    id: str
    name: str


class BaseOrjsonModel(BaseModel): 
    class Config: 
        json_loads = orjson.loads 
        json_dumps = orjson_dumps


class Film(BaseOrjsonModel):
    id: str
    imdb_rating: Optional[float]
    genre: List[str]
    title: str
    description: Optional[str]
    director: Optional[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: List[InstanceSchema]
    writers: List[InstanceSchema]


class Genre(BaseOrjsonModel):
    id: str
    name: str
    description: Optional[str]


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    role: List[str]
    film_ids: Optional[List[str]]

