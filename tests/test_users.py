import pytest
from fastapi import status
from faker import Faker

faker = Faker()


@pytest.mark.asyncio
async def test_create_user(async_client, user_data):
    request = await async_client.post("http://127.0.0.1:8000/users/", json = user_data)
    assert request.status_code == status.HTTP_200_OK
    response_json = request.json()
    assert all(user_data[check] == response_json[check] for check in ["username", "email"])

@pytest.mark.asyncio
async def test_get_user(async_client, user_data):
    request = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    response_json = request.json()
    user_id = response_json['id']
    request = await async_client.get(f"http://127.0.0.1:8000/users/{user_id}/")
    assert request.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_delete_user(async_client, user_data):
    request = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    response_json = request.json()
    user_id = response_json['id']
    delete_request = await async_client.delete(f"http://127.0.0.1:8000/users/{user_id}/")
    delete_request_json = delete_request.json()
    assert delete_request.status_code == status.HTTP_200_OK
    assert "Пользователь успешно удален" in delete_request_json['detail']


@pytest.mark.asyncio
async def test_update_user(async_client, user_data):
    request = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    response_json = request.json()
    user_id = response_json['id']
    user_update_json = {
        "username" : faker.user_name(),
        "email" : faker.email(domain = "yandex.com"),
        "id" : user_id
    }
    new_request = await async_client.patch(f"http://127.0.0.1:8000/users/update/", json = user_update_json)
    assert new_request.status_code == status.HTTP_200_OK













