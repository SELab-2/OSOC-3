from json import dumps
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings import DB_PAGE_SIZE
from src.database.models import Edition, InviteLink
from tests.utils.authorization import AuthClient


async def test_get_empty_invites(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for getting invites when db is empty"""
    await auth_client.admin()
    database_session.add(Edition(year=2022, name="ed2022"))
    await database_session.commit()

    async with auth_client:
        response = await auth_client.get("/editions/ed2022/invites", follow_redirects=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"inviteLinks": []}


async def test_get_invites(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for getting invites when db is not empty"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()
    database_session.add(InviteLink(target_email="test@ema.il", edition=edition))
    await database_session.commit()

    async with auth_client:
        response = await auth_client.get("/editions/ed2022/invites", follow_redirects=True)

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["inviteLinks"]) == 1
    link = json["inviteLinks"][0]
    assert link["id"] == 1
    assert link["email"] == "test@ema.il"


async def test_get_invites_paginated(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for getting paginated invites when db is not empty"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(InviteLink(target_email=f"{i}@example.com", edition=edition))
    await database_session.commit()

    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/invites?page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['inviteLinks']) == DB_PAGE_SIZE
        response = await auth_client.get("/editions/ed2022/invites?page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['inviteLinks']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


async def test_create_invite_valid(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for creating invites when data is valid"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        # Create POST request
        response = await auth_client.post("/editions/ed2022/invites/", content=dumps({"email": "test@ema.il"}))
        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert "mailTo" in json
        assert json["mailTo"].startswith("mailto:test@ema.il")
        assert "inviteLink" in json

        # New entry made in database
        json = (await auth_client.get("/editions/ed2022/invites/")).json()
        assert len(json["inviteLinks"]) == 1
        new_uuid = json["inviteLinks"][0]["uuid"]
        assert (await auth_client.get(f"/editions/ed2022/invites/{new_uuid}")).status_code == status.HTTP_200_OK


async def test_create_invite_invalid(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for creating invites when data is invalid"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        # Invalid POST will send invalid status code
        response = await auth_client.post("/editions/ed2022/invites/", content=dumps({"email": "invalid field"}), follow_redirects=True)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Verify that no new entry was made after the error
        assert len((await auth_client.get("/editions/ed2022/invites/", follow_redirects=True)).json()["inviteLinks"]) == 0


async def test_delete_invite_invalid(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for deleting invites when uuid is malformed"""
    await auth_client.admin()

    database_session.add(Edition(year=2022, name="ed2022"))
    await database_session.commit()

    async with auth_client:
        assert (await auth_client.delete("/editions/ed2022/invites/1")).status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_delete_invite_valid(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for deleting invites when uuid is valid"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    debug_uuid = "123e4567-e89b-12d3-a456-426614174000"

    async with auth_client:
        # Not present yet
        assert (await auth_client.delete(f"/editions/ed2022/invites/{debug_uuid}")).status_code == status.HTTP_404_NOT_FOUND

        # Create new entry in db
        invite_link = InviteLink(target_email="test@ema.il", edition=edition, uuid=UUID(debug_uuid))
        database_session.add(invite_link)
        await database_session.commit()

        # Remove
        assert (await auth_client.delete(f"/editions/ed2022/invites/{invite_link.uuid}")).status_code == status.HTTP_204_NO_CONTENT

        # Not found anymore
        assert (await auth_client.get(f"/editions/ed2022/invites/{invite_link.uuid}")).status_code == status.HTTP_404_NOT_FOUND


async def test_get_invite_malformed_uuid(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for fetching invites when uuid is malformed"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        # Verify malformed uuid (1)
        assert (await auth_client.get("/editions/ed2022/invites/1")).status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_invite_non_existing(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for fetching invites when uuid is valid but doesn't exist"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        assert (await auth_client.get("/editions/ed2022/invites/123e4567-e89b-12d3-a456-426614174000"))\
                   .status_code == status.HTTP_404_NOT_FOUND


async def test_get_invite_present(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint to fetch an invite when one is present"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    debug_uuid = "123e4567-e89b-12d3-a456-426614174000"

    # Create new entry in db
    invite_link = InviteLink(target_email="test@ema.il", edition=edition, uuid=UUID(debug_uuid))
    database_session.add(invite_link)
    await database_session.commit()

    async with auth_client:
        # Found the correct result now
        response = await auth_client.get(f"/editions/ed2022/invites/{debug_uuid}")
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json["uuid"] == debug_uuid
    assert json["email"] == "test@ema.il"


async def test_create_invite_valid_old_edition(database_session: AsyncSession, auth_client: AuthClient):
    """Test endpoint for creating invites when data is valid, but the edition is read-only"""
    await auth_client.admin()
    edition = Edition(year=2022, name="ed2022")
    edition2 = Edition(year=2023, name="ed2023")
    database_session.add(edition)
    database_session.add(edition2)
    await database_session.commit()

    async with auth_client:
        # Create POST request
        response = await auth_client.post("/editions/ed2022/invites/", content=dumps({"email": "test@ema.il"}))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
