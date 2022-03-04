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
