import pytest

from src.app.exceptions.validation_exception import ValidationException
from src.app.schemas.validators import validate_email_format, validate_edition


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


def test_edition_name():
    """Test the validation of edition names"""
    with pytest.raises(ValidationException):
        validate_edition("New Edition")

    with pytest.raises(ValidationException):
        validate_edition("NewEdition?!")

    with pytest.raises(ValidationException):
        validate_edition("(NewEdition)")

    validate_edition("Edition2022")

    validate_edition("Edition_2022")

    validate_edition("edition2022")

    validate_edition("Edition-2022")
