from sqlalchemy.orm import Session

from src.app.schemas.register import NewUser
from src.database.models import AuthEmail, CoachRequest, User, Edition

from src.app.logic.register import create_request

def test_create_request(database_session: Session): 
    edition = Edition(year = 2022)
    database_session.add(edition)
    database_session.commit()
    nu = NewUser(name="jos", email="email@email.com", pw="wachtwoord")
    create_request(database_session, nu, edition)
    
    users = database_session.query(User).where(User.name == "jos").all()
    assert len(users) == 1
    coach_requests = database_session.query(CoachRequest).where(CoachRequest.user == users[0]).all()
    auth_email = database_session.query(AuthEmail).where(AuthEmail.user == users[0]).all()
    assert len(coach_requests) == 1
    assert len(auth_email) == 1