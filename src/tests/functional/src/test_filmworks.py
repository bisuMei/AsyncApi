import pytest

from typing import List
from fastapi import status
from elasticsearch.helpers import async_bulk


def gendata(index_name: str, docs: List[dict]) -> dict:
    for doc in docs:
        yield {
            "_index": index_name,
            "_id": doc['id'],
            "_source": doc
        }


@pytest.fixture
def expected_films_list(load_test_data):
    return load_test_data('film_list.json')


@pytest.fixture
def expected_film_detail(load_test_data):
    return load_test_data('film_by_id.json')


@pytest.fixture
def load_test_films_to_es(load_test_data):
    return load_test_data('films_loads_to_es.json')


@pytest.mark.asyncio
async def test_get_list_of_films(
        es_client,
        make_get_request,
        api_films_list_v1_url,
        expected_films_list,
        load_test_films_to_es,
):

    await async_bulk(es_client, gendata('movies', load_test_films_to_es))
    response = await make_get_request(api_films_list_v1_url)

    assert response.status == status.HTTP_200_OK
    assert response.body != 0


@pytest.mark.asyncio
async def test_get_film_by_id(
        es_client,
        make_get_request,
        api_film_v1_url,
        film_id,
        expected_film_detail,
        load_test_films_to_es,
):

    await async_bulk(es_client, gendata('movies', load_test_films_to_es))
    response = await make_get_request(api_film_v1_url.format(film_id=film_id))

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_film_detail
