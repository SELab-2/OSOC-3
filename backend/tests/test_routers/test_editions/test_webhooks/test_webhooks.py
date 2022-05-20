from unittest.mock import mock_open
from uuid import UUID

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Edition, WebhookURL, Student, Skill
from tests.utils.authorization import AuthClient
from .data import create_webhook_event, WEBHOOK_EVENT_BAD_FORMAT, WEBHOOK_MISSING_QUESTION


@pytest.fixture
async def edition(database_session: AsyncSession) -> Edition:
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()
    return edition


@pytest.fixture
async def webhook(edition: Edition, database_session: AsyncSession) -> WebhookURL:
    webhook = WebhookURL(edition=edition)
    database_session.add(webhook)
    await database_session.commit()
    return webhook


@pytest.fixture
async def database_session_skills(database_session: AsyncSession) -> AsyncSession:
    """fixture to add skills"""
    database_session.add(Skill(name="Front-end developer"))
    database_session.add(Skill(name="Back-end developer"))
    database_session.add(Skill(name="UX / UI designer"))
    database_session.add(Skill(name="Graphic designer"))
    database_session.add(Skill(name="Business Modeller"))
    database_session.add(Skill(name="Storyteller"))
    database_session.add(Skill(name="Marketer"))
    database_session.add(Skill(name="Copywriter"))
    database_session.add(Skill(name="Video editor"))
    database_session.add(Skill(name="Photographer"))
    await database_session.commit()
    return database_session


async def test_new_webhook(auth_client: AuthClient, edition: Edition):
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post(f"/editions/{edition.name}/webhooks")
        assert response.status_code == status.HTTP_201_CREATED
        assert 'uuid' in response.json()
        assert UUID(response.json()['uuid'])


async def test_new_webhook_invalid_edition(auth_client: AuthClient, edition: Edition):
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/invalid/webhooks")
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_webhook(database_session_skills: AsyncSession, test_client: AsyncClient, webhook: WebhookURL):
    """test webhook"""
    
    event: dict = create_webhook_event(
        email_address="test@gmail.com",
        first_name="Bob",
        last_name="Klonck",
        preferred_name="Jhon",
        wants_to_be_student_coach=False,
        phone_number="0477002266",
    )
    async with test_client:
        response = await test_client.post(f"/editions/{webhook.edition.name}/webhooks/{webhook.uuid}", json=event)
        assert response.status_code == status.HTTP_201_CREATED

    student: Student = (await database_session_skills.execute(select(Student))).scalars().first()
    assert student.edition == webhook.edition
    assert student.email_address == "test@gmail.com"
    assert student.first_name == "Bob"
    assert student.last_name == "Klonck"
    assert student.preferred_name == "Jhon"
    assert student.wants_to_be_student_coach is False
    assert student.phone_number == "0477002266"
    assert len(student.skills) > 0


async def test_webhook_bad_format(test_client: AsyncClient, webhook: WebhookURL):
    """Test a badly formatted webhook input"""
    async with test_client:
        response = await test_client.post(
            f"/editions/{webhook.edition.name}/webhooks/{webhook.uuid}",
            json=WEBHOOK_EVENT_BAD_FORMAT
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_webhook_duplicate_email(database_session_skills: AsyncSession, test_client: AsyncClient, webhook: WebhookURL, mocker):
    """Test entering a duplicate email address"""
    mocker.patch('builtins.open', new_callable=mock_open())
    event: dict = create_webhook_event(
        email_address="test@gmail.com",
    )
    async with test_client:
        response = await test_client.post(f"/editions/{webhook.edition.name}/webhooks/{webhook.uuid}", json=event)
        assert response.status_code == status.HTTP_201_CREATED

        event: dict = create_webhook_event(
            email_address="test@gmail.com",
        )
        response = await test_client.post(f"/editions/{webhook.edition.name}/webhooks/{webhook.uuid}", json=event)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_webhook_duplicate_phone(database_session_skills: AsyncSession, test_client: AsyncClient, webhook: WebhookURL, mocker):
    """Test entering a duplicate phone number"""
    mocker.patch('builtins.open', new_callable=mock_open())
    event: dict = create_webhook_event(
        phone_number="0477002266",
    )
    async with test_client:
        response = await test_client.post(f"/editions/{webhook.edition.name}/webhooks/{webhook.uuid}", json=event)
        assert response.status_code == status.HTTP_201_CREATED

        event: dict = create_webhook_event(
            phone_number="0477002266",
        )
        response = await test_client.post(f"/editions/{webhook.edition.name}/webhooks/{webhook.uuid}", json=event)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_webhook_missing_question(database_session_skills: AsyncSession, test_client: AsyncClient, webhook: WebhookURL, mocker):
    """Test submitting a form with a question missing"""
    mocker.patch('builtins.open', new_callable=mock_open())
    async with test_client:
        response = await test_client.post(
            f"/editions/{webhook.edition.name}/webhooks/{webhook.uuid}",
            json=WEBHOOK_MISSING_QUESTION
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_new_webhook_readonly_edition(database_session_skills: AsyncSession, auth_client: AuthClient, edition: Edition):
    """Test new webhook to an old edition"""
    edition.readonly = True
    database_session_skills.add(Edition(year=2023, name="ed2023"))
    await database_session_skills.commit()
    async with auth_client:
        await auth_client.admin()
        response = await auth_client.post(f"/editions/{edition.name}/webhooks")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
