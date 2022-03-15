from sqlalchemy.orm import Session

from src.database.crud.invites import create_invite_link, delete_invite_link, get_all_pending_invites
from src.database.models import Edition, InviteLink


def test_create_invite_link(database_session: Session):
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Db empty
    assert len(get_all_pending_invites(database_session, edition)) == 0

    # Create new link
    create_invite_link(database_session, edition, "test@ema.il")

    assert len(get_all_pending_invites(database_session, edition)) == 1


def test_delete_invite_link(database_session: Session):
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Create new link
    new_link = create_invite_link(database_session, edition, "test@ema.il")

    assert len(get_all_pending_invites(database_session, edition)) == 1
    delete_invite_link(database_session, new_link)
    assert len(get_all_pending_invites(database_session, edition)) == 0


def test_get_all_pending_invites(database_session: Session):
    edition_one = Edition(year=2022)
    edition_two = Edition(year=2023)
    database_session.add(edition_one)
    database_session.add(edition_two)
    database_session.commit()

    # Db empty
    assert len(get_all_pending_invites(database_session, edition_one)) == 0
    assert len(get_all_pending_invites(database_session, edition_two)) == 0

    # Create new link
    link_one = InviteLink(target_email="test@ema.il", edition=edition_one)
    database_session.add(link_one)
    database_session.commit()

    assert len(get_all_pending_invites(database_session, edition_one)) == 1

    # Other edition still empty
    assert len(get_all_pending_invites(database_session, edition_two)) == 0

    # Add entry for other edition
    link_two = InviteLink(target_email="test@ema.il", edition=edition_two)
    database_session.add(link_two)
    database_session.commit()

    assert len(get_all_pending_invites(database_session, edition_one)) == 1
    assert len(get_all_pending_invites(database_session, edition_two)) == 1
