import json

import pytest
from fastapi.testclient import TestClient
from src.database.models import Edition, WebhookURL
from sqlalchemy.orm import Session
from starlette import status
from uuid import UUID
from .data import WEBHOOK_EVENT


@pytest.fixture
def edition(database_session: Session) -> Edition:
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    return edition


@pytest.fixture
def webhook(edition: Edition, database_session: Session) -> WebhookURL:
    webhook = WebhookURL(edition=edition)
    database_session.add(webhook)
    database_session.commit()
    return webhook


def test_new_webhook(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/{edition.edition_id}/webhooks/")
    assert response.status_code == status.HTTP_200_OK
    assert 'uuid' in response.json()
    assert UUID(response.json()['uuid'])


def test_new_webhook_invalid_edition(test_client: TestClient, edition: Edition):
    response = test_client.post(f"/editions/0/webhooks/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_webhook_trigger(test_client: TestClient, webhook: WebhookURL):
    response = test_client.post(f"/editions/{webhook.edition_id}/webhooks/")
    assert response.status_code == status.HTTP_200_OK
    uuid = response.json()['uuid']
    response = test_client.post(f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}", json=WEBHOOK_EVENT)
    assert response.status_code == status.HTTP_200_OK
