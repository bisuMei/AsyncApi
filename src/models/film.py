import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """`orjson.dumps` returns bytes, pydantic needed unicode."""
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps 