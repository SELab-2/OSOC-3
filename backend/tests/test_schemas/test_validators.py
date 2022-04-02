import pytest

from src.app.exceptions.validation_exception import ValidationException
from src.app.schemas.validators import validate_email_format


def test_email_address():
    """Test the validation of email addresses"""
    with pytest.raises(ValidationException):
        validate_email_format("test")

    with pytest.raises(ValidationException):
        validate_email_format("test@something")

    with pytest.raises(ValidationException):
        validate_email_format("test@something.")

    with pytest.raises(ValidationException):
        validate_email_format("email address with spaces")

    with pytest.raises(ValidationException):
        validate_email_format("A@Couple@Of@@s")

    validate_email_format("test.some@thi.ng")
