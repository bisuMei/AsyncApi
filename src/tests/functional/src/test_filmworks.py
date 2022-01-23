import pytest
import asyncio

from fastapi import status


@pytest.fixture
def film_id():
    return "e4626af1-7fd5-414b-ba82-5555555555"


@pytest.fixture
def genre_name():
    return "Documentary"


@pytest.fixture
def expected_films_list(load_test_data):
    return load_test_data('film_list.json')


@pytest.fixture
def expected_film_detail(load_test_data):
    return load_test_data('film_by_id.json')


@pytest.fixture
def expected_film_by_genre(load_test_data):
    return load_test_data('filter_by_genre.json')


@pytest.fixture
def expected_film_by_query(load_test_data):
    return load_test_data('film_by_query.json')


@pytest.fixture
def load_test_films_to_es(load_test_data):
    return load_test_data('films_loads_to_es.json')


@pytest.mark.asyncio
async def test_get_list_of_films(
    prepare_film_service,
    make_get_request,
    api_films_v1_url,
    expected_films_list,
    clear_redis_cache,
):
    await asyncio.sleep(1)

    response = await make_get_request(api_films_v1_url)

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_films_list


@pytest.mark.asyncio
async def test_get_film_by_id(
    prepare_film_service,
    make_get_request,
    api_film_by_id_v1_url,
    film_id,
    expected_film_detail,
    clear_redis_cache,
):
    url = api_film_by_id_v1_url.format(film_id=film_id)
    response = await make_get_request(url)

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_film_detail


@pytest.mark.asyncio
async def test_get_film_by_id_404_response(
    make_get_request,
    api_film_by_id_v1_url,
    prepare_film_service,
    clear_redis_cache,
):
    await asyncio.sleep(1)

    invalid_ids = [111, '123', '---', '+123', '}']
    for invalid_id in invalid_ids:
        url = api_film_by_id_v1_url.format(film_id=invalid_id)
        response = await make_get_request(url)
        assert response.status == status.HTTP_404_NOT_FOUND
        assert response.body == {'detail': 'Item not found'}


@pytest.mark.asyncio
async def test_film_filter_by_genre(
    prepare_film_service,
    make_get_request,
    api_films_v1_url,
    expected_film_by_genre,
    genre_name,
    clear_redis_cache,
):
    await asyncio.sleep(1)

    response = await make_get_request(api_films_v1_url, params={'filter_': genre_name})
    assert response.status == status.HTTP_200_OK
    assert response.body == expected_film_by_genre


@pytest.mark.asyncio
async def test_film_search_query(
    prepare_film_service,
    make_get_request,
    api_films_v1_url,
    expected_film_by_query,
    clear_redis_cache,
):
    await asyncio.sleep(1)

    response = await make_get_request(api_films_v1_url, params={'query': 'Leonard'})
    assert response.status == status.HTTP_200_OK
    assert response.body == expected_film_by_query
