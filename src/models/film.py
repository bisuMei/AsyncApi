import orjson

from pydantic import BaseModel
from typing import List


def orjson_dumps(v, *, default):
    """`orjson.dumps` returns bytes, pydantic needed unicode."""
    return orjson.dumps(v, default=default).decode()


class InstanceSchema(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float
    genre: List[str]
    title: str
    description: str
    director: str
    actors: List[InstanceSchema]
    writers: List[InstanceSchema]
    actors_names: List[str]
    writers_names: List[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(BaseModel):
    id: str
    full_name: str
    role: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
