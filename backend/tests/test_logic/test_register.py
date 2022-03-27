import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.app.schemas.register import NewUser
from src.database.models import AuthEmail, CoachRequest, User, Edition, InviteLink

from src.app.logic.register import create_request
from src.app.exceptions.register import FailedToAddNewUserException


def test_create_request(database_session: Session):
    """Tests if a normal request can be created"""
    edition = Edition(year=2022)
    database_session.add(edition)
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.commit()
    new_user = NewUser(name="jos", email="email@email.com",
                       pw="wachtwoord", uuid=invite_link.uuid)
    create_request(database_session, new_user, edition)

    users = database_session.query(User).where(User.name == "jos").all()
    assert len(users) == 1
    coach_requests = database_session.query(
        CoachRequest).where(CoachRequest.user == users[0]).all()
    auth_email = database_session.query(AuthEmail).where(
        AuthEmail.user == users[0]).all()
    assert len(coach_requests) == 1
    assert auth_email[0].pw_hash != new_user.pw
    assert len(auth_email) == 1


def test_duplicate_user(database_session: Session):
    """Tests if there is a duplicate, it's not created in the database"""
    edition = Edition(year=2022)
    database_session.add(edition)
    invite_link1: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    invite_link2: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.commit()
    nu1 = NewUser(name="user1", email="email@email.com",
                  pw="wachtwoord1", uuid=invite_link1.uuid)
    nu2 = NewUser(name="user2", email="email@email.com",
                  pw="wachtwoord2", uuid=invite_link2.uuid)
    create_request(database_session, nu1, edition)

    with pytest.raises(FailedToAddNewUserException):
        create_request(database_session, nu2, edition)

    # Verify that second user wasn't added
    # the first addition was successful, the second wasn't
    users = database_session.query(User).all()
    assert len(users) == 1
    assert users[0].name == nu1.name

    emails = database_session.query(AuthEmail).all()
    assert len(emails) == 1
    assert emails[0].user == users[0]

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 1
    assert requests[0].user == users[0]

    # Verify that the link wasn't removed
    links = database_session.query(InviteLink).all()
    assert len(links) == 1


def test_use_same_uuid_multiple_times(database_session: Session):
    """Tests that you can't use the same UUID multiple times"""
    edition = Edition(year=2022)
    database_session.add(edition)
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.commit()
    new_user1 = NewUser(name="jos", email="email@email.com",
                        pw="wachtwoord", uuid=invite_link.uuid)
    create_request(database_session, new_user1, edition)
    with pytest.raises(NoResultFound):
        new_user2 = NewUser(name="jos", email="email2@email.com",
                            pw="wachtwoord", uuid=invite_link.uuid)
        create_request(database_session, new_user2, edition)


def test_not_a_correct_email(database_session: Session):
    """Tests when the email is not a correct email adress, it's get the right error"""
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    with pytest.raises(ValueError):
        new_user = NewUser(name="jos", email="email", pw="wachtwoord")
        create_request(database_session, new_user, edition)
