import pytest
from fastapi.testclient import TestClient
from src.database.models import Edition
from starlette import status
from uuid import UUID


@pytest.fixture
def edition(db) -> Edition:
    edition = Edition(year=2022)
    db.add(edition)
    db.commit()
    return edition


def test_new_webhook(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/{edition.edition_id}/webhooks/")
    assert response.status_code == status.HTTP_200_OK
    assert 'uuid' in response.json()
    assert UUID(response.json()['uuid'])


def test_new_webhook_invalid_edition(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/0/webhooks/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_webhook_trigger(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/{edition.edition_id}/webhooks/")
    assert response.status_code == status.HTTP_200_OK
    uuid = response.json()['uuid']
    response = test_client.post(f"/editions/{edition.edition_id}/webhooks/{uuid}", data={})
    assert response.status_code == status.HTTP_404_NOT_FOUND
