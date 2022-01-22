import os
from environs import Env
from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Env.read_env()

# Logger Settings
logging_config.dictConfig(LOGGING)


class Config(BaseSettings):
    """Base settings"""

    PROJECT_NAME: str

    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_INDEX: dict

    REDIS_HOST: str
    REDIS_PORT: int


config = Config()
