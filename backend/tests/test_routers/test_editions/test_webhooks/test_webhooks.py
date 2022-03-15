from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Edition, WebhookURL, Student
from .data import create_webhook_event, WEBHOOK_EVENT_BAD_FORMAT, WEBHOOK_MISSING_QUESTION


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


def test_webhook(test_client: TestClient, webhook: WebhookURL, database_session: Session):
    event: dict = create_webhook_event(
        email_address="test@gmail.com",
        first_name="Bob",
        last_name="Klonck",
        preferred_name="Jhon",
        wants_to_be_student_coach=False,
        phone_number="0477002266",
    )
    response = test_client.post(f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}", json=event)
    assert response.status_code == status.HTTP_200_OK

    student: Student = database_session.query(Student).first()
    assert student.edition == webhook.edition
    assert student.email_address == "test@gmail.com"
    assert student.first_name == "Bob"
    assert student.last_name == "Klonck"
    assert student.preferred_name == "Jhon"
    assert student.wants_to_be_student_coach == False
    assert student.phone_number == "0477002266"


def test_webhook_bad_format(test_client: TestClient, webhook: WebhookURL):
    response = test_client.post(
        f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}",
        json=WEBHOOK_EVENT_BAD_FORMAT
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_webhook_duplicate_email(test_client: TestClient, webhook: WebhookURL):
    event: dict = create_webhook_event(
        email_address="test@gmail.com",
    )
    response = test_client.post(f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}", json=event)
    assert response.status_code == status.HTTP_200_OK

    event: dict = create_webhook_event(
        email_address="test@gmail.com",
    )
    response = test_client.post(f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}", json=event)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_webhook_duplicate_phone(test_client: TestClient, webhook: WebhookURL):
    event: dict = create_webhook_event(
        phone_number="0477002266",
    )
    response = test_client.post(f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}", json=event)
    assert response.status_code == status.HTTP_200_OK

    event: dict = create_webhook_event(
        phone_number="0477002266",
    )
    response = test_client.post(f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}", json=event)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_webhook_missing_question(test_client: TestClient, webhook: WebhookURL):
    response = test_client.post(
        f"/editions/{webhook.edition_id}/webhooks/{webhook.uuid}",
        json=WEBHOOK_MISSING_QUESTION
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY