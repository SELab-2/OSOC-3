from dataclasses import dataclass
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
    preferred_name: str | None
    email_address: str
    phone_number: str
    alumni: bool
    decision: DecisionEnum = Field(
        DecisionEnum.UNDECIDED, alias="finalDecision")
    wants_to_be_student_coach: bool
    edition_id: int

    skills: list[Skill]
    nr_of_suggestions: Suggestions | None = None

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


@dataclass
class CommonQueryParams:
    """search query paramaters"""
    name: str = ""
    alumni: bool = False
    student_coach: bool = False
    skill_ids: list[int] = Query([])
    own_suggestions: bool = False
    decisions: list[DecisionEnum] = Query([])
    page: int = 0


@dataclass
class EmailsSearchQueryParams:
    """search query paramaters for email"""
    name: str = ""
    email_status: list[EmailStatusEnum] = Query([])
    page: int = 0


class DecisionEmail(CamelCaseModel):
    """
    Model to represent DecisionEmail
    """
    email_id: int
    decision: EmailStatusEnum
    date: datetime

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ReturnStudentMailList(CamelCaseModel):
    """
    Model to return a list of mails of a student
    """
    student: Student
    emails: list[DecisionEmail]


class ListReturnStudentMailList(CamelCaseModel):
    """Model to give a list of ReturnStudentMailList"""
    student_emails: list[ReturnStudentMailList]


class NewEmail(CamelCaseModel):
    """The fields of a DecisionEmail"""
    students_id: list[int]
    email_status: EmailStatusEnum
