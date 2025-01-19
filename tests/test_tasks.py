from datetime import datetime, timedelta

import pytest
from faker import Faker
from fastapi import status

from app.database import settings

ENDPOINT = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/api/v1"
faker = Faker()


@pytest.mark.asyncio
async def test_create_task(async_client, user_data, task_data):

    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK

    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(
        f"{ENDPOINT}/tasks/me/", json=task_data, headers=headers
    )
    assert task_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_task(async_client, user_data, task_data):

    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK

    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(
        f"{ENDPOINT}/tasks/me/", json=task_data, headers=headers
    )
    assert task_request.status_code == status.HTTP_200_OK

    assert all(
        task_request.json()[check] == task_data[check]
        for check in ["description", "title"]
    )

    task_get_request = await async_client.get(f"{ENDPOINT}/tasks/me/", headers=headers)
    assert task_get_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_all_tasks(async_client, user_data, task_data):

    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK

    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(
        f"{ENDPOINT}/tasks/me/", json=task_data, headers=headers
    )
    assert task_request.status_code == status.HTTP_200_OK
    task_delete_request = await async_client.delete(
        f"{ENDPOINT}/tasks/me/", headers=headers
    )
    assert task_delete_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_task(async_client, user_data, task_data):

    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK

    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(
        f"{ENDPOINT}/tasks/me/", json=task_data, headers=headers
    )
    assert task_request.status_code == status.HTTP_200_OK
    task_id = task_request.json()["id"]
    task_delete_request = await async_client.delete(
        f"{ENDPOINT}/tasks/me/{task_id}/", headers=headers
    )
    assert task_delete_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_change_status_task(async_client, user_data, task_data):

    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK

    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(
        f"{ENDPOINT}/tasks/me/", json=task_data, headers=headers
    )
    assert task_request.status_code == status.HTTP_200_OK
    task_id = task_request.json()["id"]
    change_status_task_json = {"id": task_id, "new_status": "in_progress"}
    task_change_status_request = await async_client.put(
        f"{ENDPOINT}/tasks/me/{task_id}/status/",
        headers=headers,
        json=change_status_task_json,
    )
    assert task_change_status_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_task(async_client, user_data, task_data):

    create_user_response = await async_client.post(
        f"{ENDPOINT}/users/register/", json=user_data
    )
    assert create_user_response.status_code == status.HTTP_200_OK

    response = await async_client.post(
        f"{ENDPOINT}/users/login/",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(
        f"{ENDPOINT}/tasks/me/", json=task_data, headers=headers
    )
    assert task_request.status_code == status.HTTP_200_OK
    task_id = task_request.json()["id"]
    update_task_json = {
        "id": task_id,
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=100),
        "deadline": (
            datetime.now() + timedelta(days=faker.random_int(min=1, max=10))
        ).isoformat(),
    }

    update_task_response = await async_client.patch(
        f"{ENDPOINT}/tasks/me/update/", json=update_task_json, headers=headers
    )
    assert update_task_response.status_code == status.HTTP_200_OK
