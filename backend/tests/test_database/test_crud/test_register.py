from sqlalchemy.orm import Session

from src.database.models import Edition, User

from src.database.crud.register import create_user

def test_test(database_session: Session):
    create_user(Session, "jos", "mail@email.com")

    a = database_session.query(User).all()
    print(len(a))
    assert False
