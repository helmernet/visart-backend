from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "user1"
    assert response.json()["email"] == "user1@example.com"
