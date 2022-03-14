import imp
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.database.models import Edition, User

from src.database.crud.register import create_user

def test_test(database_session: Session):
    database_session.add(Edition(year=2022))
    database_session.commit()
    a = database_session.query(Edition).where(Edition.year == 2022).all()
    assert len(a) == 1
    edition = a[0]

    create_user(Session, edition, "jos", "mail@email.com")

    a = database_session.query(User).all()
    print(len(a))
    assert False
