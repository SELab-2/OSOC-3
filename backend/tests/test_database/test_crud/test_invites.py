from uuid import UUID

import pytest
import sqlalchemy.exc
from sqlalchemy.orm import Session

from src.app.exceptions.parsing import MalformedUUIDError
from src.database.crud.invites import create_invite_link, delete_invite_link, get_all_pending_invites, \
    get_invite_link_by_uuid
from src.database.models import Edition, InviteLink


def test_create_invite_link(database_session: Session):
    """Test creation of new invite links"""
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Db empty
    assert len(get_all_pending_invites(database_session, edition)) == 0

    # Create new link
    create_invite_link(database_session, edition, "test@ema.il")

    assert len(get_all_pending_invites(database_session, edition)) == 1


def test_delete_invite_link(database_session: Session):
    """Test deletion of existing invite links"""
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Create new link
    new_link = create_invite_link(database_session, edition, "test@ema.il")

    assert len(get_all_pending_invites(database_session, edition)) == 1
    delete_invite_link(database_session, new_link)
    assert len(get_all_pending_invites(database_session, edition)) == 0


def test_get_all_pending_invites_empty(database_session: Session):
    """Test fetching all invites for a given edition when db is empty"""
    edition_one = Edition(year=2022)
    edition_two = Edition(year=2023)
    database_session.add(edition_one)
    database_session.add(edition_two)
    database_session.commit()

    # Db empty
    assert len(get_all_pending_invites(database_session, edition_one)) == 0
    assert len(get_all_pending_invites(database_session, edition_two)) == 0


def test_get_all_pending_invites_one_present(database_session: Session):
    """
    Test fetching all invites for two editions when only one of them
    has valid entries
    """
    edition_one = Edition(year=2022)
    edition_two = Edition(year=2023)
    database_session.add(edition_one)
    database_session.add(edition_two)
    database_session.commit()

    # Create new link
    link_one = InviteLink(target_email="test@ema.il", edition=edition_one)
    database_session.add(link_one)
    database_session.commit()

    assert len(get_all_pending_invites(database_session, edition_one)) == 1

    # Other edition still empty
    assert len(get_all_pending_invites(database_session, edition_two)) == 0


def test_get_all_pending_invites_two_present(database_session: Session):
    """Test fetching all links for two editions when both of them have data"""
    edition_one = Edition(year=2022)
    edition_two = Edition(year=2023)
    database_session.add(edition_one)
    database_session.add(edition_two)
    database_session.commit()

    # Create new links
    link_one = InviteLink(target_email="test@ema.il", edition=edition_one)
    link_two = InviteLink(target_email="test@ema.il", edition=edition_two)
    database_session.add(link_one)
    database_session.add(link_two)
    database_session.commit()

    assert len(get_all_pending_invites(database_session, edition_one)) == 1
    assert len(get_all_pending_invites(database_session, edition_two)) == 1


def test_get_invite_link_by_uuid_existing(database_session: Session):
    """Test fetching links by uuid's when it exists"""
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    debug_uuid = "123e4567-e89b-12d3-a456-426614174000"
    new_link = InviteLink(target_email="test@ema.il", edition=edition, uuid=UUID(debug_uuid))
    database_session.add(new_link)
    database_session.commit()

    assert get_invite_link_by_uuid(database_session, debug_uuid).invite_link_id == new_link.invite_link_id


def test_get_invite_link_by_uuid_non_existing(database_session: Session):
    """Test fetching links by uuid's when they don't exist"""
    # Db empty
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        get_invite_link_by_uuid(database_session, "123e4567-e89b-12d3-a456-426614174011")

    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    debug_uuid = "123e4567-e89b-12d3-a456-426614174000"
    new_link = InviteLink(target_email="test@ema.il", edition=edition, uuid=UUID(debug_uuid))
    database_session.add(new_link)
    database_session.commit()

    # Non-existent id
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        get_invite_link_by_uuid(database_session, "123e4567-e89b-12d3-a456-426614174011")


def test_get_invite_link_by_uuid_malformed(database_session: Session):
    """Test fetching a link by its uuid when the id is malformed"""
    with pytest.raises(MalformedUUIDError):
        get_invite_link_by_uuid(database_session, "some malformed string that isn't a UUID")
