"""Useful functions that can be used for validation of fields"""
import re

from src.app.exceptions.validation_exception import ValidationException


def validate_email_format(email_address: str):
    """Regex that checks if an email address is well-formed
    This can't check if an email address is actually real, the only way
    to check that is to send something to the address and make the user
    click on a verification link of some sorts.
    """
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email_address):
        raise ValidationException("Malformed email address.")


def validate_edition(edition: str):
    """
    An edition should not contain any spaces in order for us to use it in
    the path of various resources, this function checks that.
    """
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", edition):
        raise ValidationException("Spaces detected in the edition name")
