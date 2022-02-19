"""Test settings."""
import os

from environs import Env

from pydantic import BaseSettings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Env.read_env()


class Config(BaseSettings):
    """Test settings"""

    SERVICE_HOST: str
    SERVICE_PORT: int

    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_INDEX: dict

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_SECRET: str


config = Config()
