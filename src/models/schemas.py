import orjson

from pydantic import BaseModel
from typing import List, Optional


def orjson_dumps(v, *, default):
    """`orjson.dumps` returns bytes, pydantic needed unicode."""
    return orjson.dumps(v, default=default).decode()


class InstanceSchema(BaseModel):
    id: str
    name: str


class FilmShort(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    
    class Config:
        fields = {'field_value': 'fields'}


class GenreShort(BaseModel):
    id: str
    name: str

    class Config:
        fields = {'field_value': 'fields'}


class Film(BaseModel):
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

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(BaseModel):
    id: str
    name: str
    description: Optional[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(BaseModel):
    id: str
    full_name: str
    role: List[str]
    film_ids: Optional[List[str]]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
