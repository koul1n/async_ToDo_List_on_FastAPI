import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_task(async_client, user_data, task_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    assert create_user_response.status_code == status.HTTP_200_OK
    user_id = create_user_response.json()['id']
    # Логинимся
    response = await async_client.post("http://127.0.0.1:8000/users/login/", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data, headers=headers)
    assert task_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_task(async_client, user_data, task_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    assert create_user_response.status_code == status.HTTP_200_OK
    user_id = create_user_response.json()['id']
    # Логинимся
    response = await async_client.post("http://127.0.0.1:8000/users/login/", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data, headers=headers)
    assert task_request.status_code == status.HTTP_200_OK

    assert all(task_request.json()[check] == task_data[check] for check in ["description", "title"])

    task_get_request = await async_client.get(f"http://127.0.0.1:8000/tasks/{user_id}/", headers=headers)
    assert task_get_request.status_code == status.HTTP_200_OK



@pytest.mark.asyncio
async def test_delete_all_tasks(async_client, user_data, task_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    assert create_user_response.status_code == status.HTTP_200_OK
    user_id = create_user_response.json()['id']
    # Логинимся
    response = await async_client.post("http://127.0.0.1:8000/users/login/", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data, headers=headers)
    assert task_request.status_code == status.HTTP_200_OK
    task_delete_request = await async_client.delete(f"http://127.0.0.1:8000/tasks/{user_id}/", headers=headers)
    assert task_delete_request.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_task(async_client, user_data, task_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    assert create_user_response.status_code == status.HTTP_200_OK
    user_id = create_user_response.json()['id']
    # Логинимся
    response = await async_client.post("http://127.0.0.1:8000/users/login/", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data, headers=headers)
    assert task_request.status_code == status.HTTP_200_OK
    task_id = task_request.json()['id']
    task_delete_request = await async_client.delete(f"http://127.0.0.1:8000/tasks/{user_id}/{task_id}/", headers=headers)
    assert task_delete_request.status_code == status.HTTP_200_OK



@pytest.mark.asyncio
async def test_complete_task(async_client, user_data, task_data):
    # Сначала создаем пользователя
    create_user_response = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    assert create_user_response.status_code == status.HTTP_200_OK
    user_id = create_user_response.json()['id']
    # Логинимся
    response = await async_client.post("http://127.0.0.1:8000/users/login/", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    token = response_json['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    task_request = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data, headers=headers)
    assert task_request.status_code == status.HTTP_200_OK
    task_id = task_request.json()['id']
    task_complete_request = await async_client.put(f"http://127.0.0.1:8000/tasks/{user_id}/{task_id}/complete/", headers=headers)
    assert task_complete_request.status_code == status.HTTP_200_OK
    assert task_complete_request.json()['is_completed'] is True

