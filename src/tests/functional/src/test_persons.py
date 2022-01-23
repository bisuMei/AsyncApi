import asyncio

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_list_of_persons(
    prepare_person_service,
    make_get_request,
    clear_redis_cache,
    api_persons_v1_url,
    expected_persons_list,
):
    await asyncio.sleep(1)

    response = await make_get_request(api_persons_v1_url)

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_persons_list


@pytest.mark.asyncio
async def test_get_person_by_id(
    prepare_person_service,
    make_get_request,
    clear_redis_cache,
    api_person_by_id_v1_url,
    expected_person_detail,
    person_id,
):
    url = api_person_by_id_v1_url.format(person_id=person_id)
    response = await make_get_request(url)

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_person_detail[0]


@pytest.mark.asyncio
async def test_get_person_by_id_404_response(
    prepare_person_service,
    make_get_request,
    clear_redis_cache,
    api_person_by_id_v1_url,
):
    invalid_person_ids = ['123', 123, '->', '-123+']
    for invalid_id in invalid_person_ids:
        url = api_person_by_id_v1_url.format(person_id=invalid_id)
        response = await make_get_request(url)

        assert response.status == status.HTTP_404_NOT_FOUND
        assert response.body == {'detail': 'Item not found'}


@pytest.mark.asyncio
async def test_film_search_by_person_id(
    prepare_film_service,
    prepare_person_service,
    make_get_request,
    clear_redis_cache,
    api_search_film_by_person,
    person_id,
    expected_film_by_person,
):
    await asyncio.sleep(1)

    url = api_search_film_by_person.format(person_id=person_id)
    response = await make_get_request(url)

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_film_by_person


@pytest.mark.asyncio
async def test_person_search_by_query(
    prepare_person_service,
    make_get_request,
    api_persons_v1_url,
    clear_redis_cache,
    expected_person_detail,
):
    await asyncio.sleep(1)

    response = await make_get_request(api_persons_v1_url, params={'query': 'Driver'})
    assert response.status == status.HTTP_200_OK
    assert response.body == expected_person_detail

