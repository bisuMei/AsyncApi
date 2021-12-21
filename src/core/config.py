import os
from logging import config as logging_config
from typing import cast

from core.logger import LOGGING
from decouple import config


# Logger Settings
logging_config.dictConfig(LOGGING)


PROJECT_NAME = config('PROJECT_NAME')


# Redis Settings
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT', cast=int)


# Elasticsearch Settings
ELASTIC_HOST = config('ELASTIC_HOST')
ELASTIC_PORT = config('ELASTIC_PORT', cast=int)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 