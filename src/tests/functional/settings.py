"""Test settings."""
import os


SERVICE_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
SERVICE_URL = f'http://{SERVICE_HOST}:8000'

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
ELASTIC_URL = f'http://{ELASTIC_HOST}:{ELASTIC_PORT}'