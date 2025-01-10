import pytest
from fastapi import status
from faker import Faker

fake = Faker()

ENDPOINT = 'http://127.0.0.1:8000/api/v1'

@pytest.mark.asyncio
async def test_create_user(async_client, user_data):
    request = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert request.status_code == status.HTTP_200_OK
    response_json = request.json()
    assert all(
        user_data[check] == response_json[check] for check in ["username", "email"]
    )


@pytest.mark.asyncio
async def test_login_user(async_client, user_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK
    # Логинимся
    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert "access_token" in response_json
    assert response_json["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_get_user(async_client, user_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK
    # Логинимся
    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    get_request = await async_client.get(
        f"{ENDPOINT}/users/me/", headers=headers
    )
    assert get_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_user(async_client, user_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK
    # Логинимся
    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    delete_request = await async_client.delete(
        f"{ENDPOINT}/users/me/delete/", headers=headers
    )
    assert delete_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_user(async_client, user_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK
    # Логинимся
    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    data = {"username": fake.user_name(), "email": fake.email()}
    update_request = await async_client.patch(
        f"{ENDPOINT}/users/me/update/", headers=headers, json=data
    )
    assert update_request.status_code == status.HTTP_200_OK
