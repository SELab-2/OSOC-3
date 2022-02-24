import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class RoleEnum(enum.Enum):
    """Enum for the different roles a user can have
    """
    ADMIN = 0
    COACH = 1


class User(Base):
    """Table that stores users of the tool (only admins & coaches)"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(RoleEnum))
