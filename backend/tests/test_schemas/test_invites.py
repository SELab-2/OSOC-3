import pytest
from pydantic import ValidationError

from src.app.schemas.invites import EmailAddress


def test_email_address():
    with pytest.raises(ValidationError):
        EmailAddress(email="test")

    with pytest.raises(ValidationError):
        EmailAddress(email="test@something")

    with pytest.raises(ValidationError):
        EmailAddress(email="test@something.")

    EmailAddress(email="test.some@thi.ng")
