from fastapi.testclient import TestClient


def test_get_users(test_client: TestClient):
    response = test_client.get("/editions/123/users/")
    print(response.status_code)
    print(response.json())
