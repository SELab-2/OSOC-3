from datetime import timedelta
from typing import Text

from requests import Response
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.app.logic.security import create_access_token
from src.database.models import User, Edition


class AuthClient(TestClient):
    """Custom TestClient that handles authentication to make tests more compact"""
    user: User | None = None
    headers: dict[str, str] | None = None
    session: Session

    def __init__(self, session: Session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session

    def invalid(self):
        """Sign in with an invalid access token"""
        self.headers = {
            "Authorization": "Bearer If I can't scuba, then what has this all been about? What am I working towards?"
        }

    def admin(self):
        """Sign in as an admin for all future requests"""
        # Create a new user in the db
        admin = User(name="Pytest Admin", email="admin@pytest.email", admin=True)
        self.session.add(admin)
        self.session.commit()

        self.login(admin)

    def coach(self, edition: Edition):
        """Sign in as a coach for all future requests
        Assigns the coach to the edition
        """
        # Create a new user in the db
        coach = User(name="Pytest Coach", email="coach@pytest.email", admin=False)

        # Link the coach to the edition
        coach.editions.append(edition)
        self.session.add(coach)
        self.session.commit()

        self.login(coach)

    def login(self, user: User):
        """Sign in as a user for all future requests"""
        self.user = user

        access_token_expires = timedelta(hours=24)
        access_token = create_access_token(
            data={"sub": str(user.user_id)}, expires_delta=access_token_expires
        )

        # Add auth headers into dict
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def delete(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return super().delete(url, **kwargs)

    def get(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return super().get(url, **kwargs)

    def patch(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return super().patch(url, **kwargs)

    def post(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return super().post(url, **kwargs)

    def put(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return super().put(url, **kwargs)
