import pytest
from fastapi import status
import random


@pytest.mark.asyncio
async def test_create_task(task_data, user_data, async_client):
    request_user = await async_client.post("http://127.0.0.1:8000/users/", json = user_data)
    assert request_user.status_code == status.HTTP_200_OK
    response_json_user = request_user.json()
    user_id = response_json_user['id']
    request_task = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data)
    assert request_task.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_complete_and_delete_task(task_data, async_client, user_data):
    request_user = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    assert request_user.status_code == status.HTTP_200_OK
    response_json_user = request_user.json()
    user_id = response_json_user['id']
    request_task = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data)
    assert request_task.status_code == status.HTTP_200_OK
    request_task_json = request_task.json()
    task_id = request_task_json['id']
    request_complete_task = await async_client.put(f"http://127.0.0.1:8000/tasks/{user_id}/{task_id}/complete/")
    assert request_complete_task.status_code == status.HTTP_200_OK
    request_complete_task_json = request_complete_task.json()
    assert request_complete_task_json['is_completed'] == True
    request_delete_task = await async_client.delete(f"http://127.0.0.1:8000/tasks/{user_id}/{task_id}/")
    assert request_delete_task.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_delete_all_tasks(task_data,user_data,async_client):
    request_user = await async_client.post("http://127.0.0.1:8000/users/", json=user_data)
    assert request_user.status_code == status.HTTP_200_OK
    response_json_user = request_user.json()
    user_id = response_json_user['id']
    for count_tasks in range(random.randint(2,5)):
        request_task = await async_client.post(f"http://127.0.0.1:8000/tasks/{user_id}/", json=task_data)
        assert request_task.status_code == status.HTTP_200_OK
    request_delete_all_tasks = await async_client.delete(f"http://127.0.0.1:8000/tasks/{user_id}/")
    assert request_delete_all_tasks.status_code == status.HTTP_200_OK
    request_delete_all_tasks_json = request_delete_all_tasks.json()
    assert request_delete_all_tasks_json['message'] == "Все задачи удалены."








