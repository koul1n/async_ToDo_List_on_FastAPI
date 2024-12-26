

def test_create_user(user_data, client):
    response = client.post("http://127.0.0.1:8000/users/", json = user_data)
    assert response.status_code == 200
    assert user_data["username"] == response.json()["username"]

