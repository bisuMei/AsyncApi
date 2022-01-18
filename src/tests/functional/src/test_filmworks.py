import pytest

from core import config
from fastapi import status

from tests.functional.utils.elastic_test_service import ElasticTestService
from tests.functional.utils.elastic_test_schemas import filmworks_index_schema


@pytest.fixture
def expected_films_list(load_test_data):
    return load_test_data('film_list.json')


@pytest.fixture
def expected_film_detail(load_test_data):
    return load_test_data('film_by_id.json')


@pytest.fixture
def load_test_films_to_es(load_test_data):
    return load_test_data('films_loads_to_es.json')


@pytest.fixture
def prepare_service(es_client, load_test_films_to_es):
    """Create test index for tests and delete index after."""
    es_service = ElasticTestService(es_client)
    es_service.create_index(config.ELASTIC_INDEX['movies'], filmworks_index_schema)
    es_service.bulk_store(config.ELASTIC_INDEX['movies'], load_test_films_to_es)
    yield
    es_service.delete_index(config.ELASTIC_INDEX['movies'])


class TestFilmService:

    @pytest.mark.asyncio
    async def test_get_list_of_films(
            self,
            make_get_request,
            api_films_list_v1_url,
            expected_films_list,
            prepare_service,
    ):
        response = await make_get_request(api_films_list_v1_url)

        assert response.status == status.HTTP_200_OK
        assert response.body == expected_films_list

    @pytest.mark.asyncio
    async def test_get_film_by_id(
            self,
            prepare_service,
            make_get_request,
            api_film_v1_url,
            film_id,
            expected_film_detail,
    ):
        response = await make_get_request(api_film_v1_url.format(film_id=film_id))

        assert response.status == status.HTTP_200_OK
        assert response.body == expected_film_detail
