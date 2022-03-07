from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_users():
    response = client.get("/editions/123/users/")
    print(response.status_code)
    print(response.json())
