from sqlalchemy.orm import Session

from src.database.models import AuthEmail, CoachRequest, User, Edition

from src.database.crud.register import create_user, create_coach_request, create_auth_email

def test_create_user(database_session: Session):
    create_user(database_session, "jos", "mail@email.com")

    a = database_session.query(User).where(User.name == "jos").all()
    assert len(a) == 1
    assert a[0].name == "jos"
    assert a[0].email == "mail@email.com"

def test_react_coach_request(database_session: Session):
    edition = Edition(year = 2022)
    database_session.add(edition)
    database_session.commit()
    u = create_user(database_session, "jos", "mail@email.com")
    
    create_coach_request(database_session, u, edition)
    a = database_session.query(CoachRequest).where(CoachRequest.user == u).all()

    assert len(a) == 1
    assert a[0].user_id == u.user_id 
    assert a[0].user == u
    assert u.coach_request == a[0]

def test_create_auth_email(database_session: Session):
    u = create_user(database_session, "jos", "mail@email.com")
    create_auth_email(database_session, u, "wachtwoord")

    a = database_session.query(AuthEmail).where(AuthEmail.user == u).all()
    
    assert len(a) == 1
    assert a[0].user_id == u.user_id
    assert a[0].user == u
    assert a[0].pw_hash != "wachtwoord"
    assert u.email_auth == a[0]
