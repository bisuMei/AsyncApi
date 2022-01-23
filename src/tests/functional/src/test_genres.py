import asyncio

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_list_of_genres(
    prepare_genre_service,
    make_get_request,
    clear_redis_cache,
    api_genre_v1_url,
    expected_genres_list,
):
    await asyncio.sleep(1)

    response = await make_get_request(api_genre_v1_url)

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_genres_list


@pytest.mark.asyncio
async def test_get_genre_by_id(
    prepare_genre_service,
    make_get_request,
    clear_redis_cache,
    api_genre_by_id_v1_url,
    expected_genre_detail,
    genre_id,
):
    await asyncio.sleep(1)

    url = api_genre_by_id_v1_url.format(genre_id=genre_id)
    response = await make_get_request(url)

    assert response.status == status.HTTP_200_OK
    assert response.body == expected_genre_detail


@pytest.mark.asyncio
async def test_get_genre_by_id_404_response(
    prepare_genre_service,
    make_get_request,
    clear_redis_cache,
    api_genre_by_id_v1_url,
):
    invalid_genre_ids = ['123', 123, '->', '-123+']
    for invalid_id in invalid_genre_ids:
        url = api_genre_by_id_v1_url.format(genre_id=invalid_id)
        response = await make_get_request(url)

        assert response.status == status.HTTP_404_NOT_FOUND
        assert response.body == {'detail': 'Item not found'}




