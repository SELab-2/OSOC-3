"""
Note: the actual values of the enums are NOT used in the database, only the names of the fields
"""
import enum
from typing import Any


@enum.unique
class DecisionEnum(enum.Enum):
    """Enum for a decision made by a coach or admin"""
    UNDECIDED = 0
    YES = 1
    MAYBE = 2
    NO = 3


@enum.unique
class RoleEnum(enum.Enum):
    """Enum for the different roles a user can have"""
    ADMIN = 0
    COACH = 1
    DISABLED = 2


@enum.unique
class QuestionEnum(enum.Enum):
    """Enum for the different question types in a Form"""
    CHECKBOXES = "CHECKBOXES"
    FILE_UPLOAD = "FILE_UPLOAD"
    INPUT_EMAIL = "INPUT_EMAIL"
    INPUT_LINK = "INPUT_LINK"
    INPUT_PHONE_NUMBER = "INPUT_PHONE_NUMBER"
    INPUT_TEXT = "INPUT_TEXT"
    INPUT_NUMBER = "INPUT_NUMBER"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TEXTAREA = "TEXTAREA"

    UNKNOWN = None  # Returned when no specific question can be matched

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return QuestionEnum.UNKNOWN
