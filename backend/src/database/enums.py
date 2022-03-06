"""
Note: the actual values of the enums are NOT used in the database, only the names of the fields
"""
import enum


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
    CHECKBOXES = 0
    FILE_UPLOAD = 1
    INPUT_EMAIL = 2
    INPUT_LINK = 3
    INPUT_PHONE_NUMBER = 4
    INPUT_TEXT = 5
    MULTIPLE_CHOICE = 6
    TEXTAREA = 7

