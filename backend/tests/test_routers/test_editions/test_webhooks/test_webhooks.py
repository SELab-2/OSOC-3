import pytest
from fastapi.testclient import TestClient
from src.database.models import Edition
from uuid import UUID


@pytest.fixture
def edition(database_session) -> Edition:
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    return edition


def test_new_webhook(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/{edition.edition_id}/webhooks/")
    assert response.status_code == 200
    assert 'uuid' in response.json()
    assert UUID(response.json()['uuid'])


def test_new_webhook_invalid_edition(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/0/webhooks/")
    assert response.status_code == 404


def test_webhook_trigger(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/{edition.edition_id}/webhooks/")
    assert response.status_code == 200
    uuid = response.json()['uuid']
    response = test_client.post(f"/editions/{edition.edition_id}/webhooks/{uuid}", data={})
    assert response.status_code == 404
