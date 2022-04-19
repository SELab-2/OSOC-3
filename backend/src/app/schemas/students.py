# pylint: disable=too-many-arguments
from datetime import datetime
from fastapi import Query
from pydantic import Field

from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum, EmailStatusEnum
from src.app.schemas.skills import Skill


class NewDecision(CamelCaseModel):
    """the fields of a decision"""
    decision: DecisionEnum


class Suggestions(CamelCaseModel):
    """
    Model to represent to number of suggestions organised by type
    """
    yes: int
    maybe: int
    no: int


class Student(CamelCaseModel):
    """
    Model to represent a Student
    Sent as a response to API /GET requests
    """
    student_id: int
    first_name: str
    last_name: str
    preferred_name: str
    email_address: str
    phone_number: str
    alumni: bool
    decision: DecisionEnum = Field(
        DecisionEnum.UNDECIDED, alias="finalDecision")
    wants_to_be_student_coach: bool
    edition_id: int

    skills: list[Skill]
    nr_of_suggestions: Suggestions = None

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ReturnStudent(CamelCaseModel):
    """
    Model to return a student
    """
    student: Student


class ReturnStudentList(CamelCaseModel):
    """
    Model to return a list of students
    """
    students: list[Student]


class CommonQueryParams:
    """search query paramaters"""

    def __init__(self, first_name: str = "", last_name: str = "", alumni: bool = False,
                 student_coach: bool = False, skill_ids: list[int] = Query([])) -> None:
        """init"""
        self.first_name = first_name
        self.last_name = last_name
        self.alumni = alumni
        self.student_coach = student_coach
        self.skill_ids = skill_ids


class DecisionEmail(CamelCaseModel):
    """
    Model to represent DecisionEmail
    """
    email_id: int
    student_id: int
    decision: EmailStatusEnum
    date: datetime

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ReturnStudentMailList(CamelCaseModel):
    """
    Model to return a list of mails of a student
    """
    emails: list[DecisionEmail]
