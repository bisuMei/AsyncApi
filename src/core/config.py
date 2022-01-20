import os
from logging import config as logging_config

from src.core.logger import LOGGING


# Logger Settings
logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')


# Redis Settings
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))


# Elasticsearch Settings
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
ELASTIC_INDEX = os.getenv('ELASTIC_INDEX', {'movies': 'movies', 'persons': 'persons', 'genres': 'genres'})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
