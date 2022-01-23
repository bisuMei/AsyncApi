"""Fixtures for filmworks service tests."""
import pytest

from tests.functional.settings import config
from tests.functional.utils.elastic_test_schemas import filmworks_index_schema
from tests.functional.utils.elastic_test_service import ElasticTestService


@pytest.fixture
async def prepare_film_service(es_client, load_test_films_to_es):
    """Create test index for tests and delete index after."""
    es_service = ElasticTestService(es_client)
    await es_service.create_index(config.ELASTIC_INDEX['movies'], filmworks_index_schema)
    await es_service.bulk_store(config.ELASTIC_INDEX['movies'], load_test_films_to_es)
    yield
    await es_service.delete_index(config.ELASTIC_INDEX['movies'])


@pytest.fixture
def load_test_films_to_es(load_test_data):
    return load_test_data('films_loads_to_es.json')


@pytest.fixture
def api_films_v1_url():
    return '/api/v1/film/'


@pytest.fixture
def api_film_by_id_v1_url():
    return '/api/v1/film/{film_id}'


@pytest.fixture
def film_id():
    return "e4626af1-7fd5-414b-ba82-5555555555"


@pytest.fixture
def genre_name():
    return "Adventure"


@pytest.fixture
def expected_films_list(load_test_data):
    return load_test_data('film_list.json')


@pytest.fixture
def expected_film_detail(load_test_data):
    return load_test_data('film_by_id.json')


@pytest.fixture
def expected_film_search(load_test_data):
    return load_test_data('film_search.json')
