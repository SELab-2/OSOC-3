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
