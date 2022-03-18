from datetime import timedelta
from typing import Text

from requests import Response
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.app.logic.security import create_access_token
from src.database.models import User


class AuthClient(TestClient):
    """Custom TestClient that handles authentication to make tests more compact"""
    user: User | None = None
    headers: dict[str, str] | None = None
    session: Session

    def __init__(self, session: Session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session

    def admin(self):
        """Sign in as an admin for all future requests"""
        # Create a new user in the db
        admin = User(name="Pytest Admin", email="admin@pytest.email", admin=True)
        self.session.add(admin)
        self.session.commit()

        self.login(admin)

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
