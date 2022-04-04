from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.app.logic import security
from src.database.models import AuthEmail, User


def test_login_non_existing(test_client: TestClient):
    """Test logging in without an existing account"""
    form = {
        "username": "this user",
        "password": "does not exist"
    }

    assert test_client.post("/login/token", data=form).status_code == status.HTTP_401_UNAUTHORIZED


def test_login_existing(database_session: Session, test_client: TestClient):
    """Test logging in with an existing account"""
    email = "test@ema.il"
    password = "password"

    # Create new user & auth entries in db
    user = User(name="test")

    database_session.add(user)
    database_session.commit()

    auth = AuthEmail(pw_hash=security.get_password_hash(password), email=email)
    auth.user = user
    database_session.add(auth)
    database_session.commit()

    # Try to get a token using the credentials for the new user
    form = {
        "username": email,
        "password": password
    }

    assert test_client.post("/login/token", data=form).status_code == status.HTTP_200_OK


def test_login_existing_wrong_credentials(database_session: Session, test_client: TestClient):
    """Test logging in with existing, but wrong credentials"""
    email = "test@ema.il"
    password = "password"

    # Create new user & auth entries in db
    user = User(name="test")

    database_session.add(user)
    database_session.commit()

    auth = AuthEmail(pw_hash=security.get_password_hash(password), email=email)
    auth.user = user
    database_session.add(auth)
    database_session.commit()

    # Try to get a token using the credentials for the new user
    form = {
        "username": email,
        "password": "another password"
    }

    assert test_client.post("/login/token", data=form).status_code == status.HTTP_401_UNAUTHORIZED
