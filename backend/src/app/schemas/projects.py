from pydantic import BaseModel

from src.app.schemas.utils import CamelCaseModel
from src.database.enums import DecisionEnum


class User(CamelCaseModel):
    """Represents a User from the database"""
    user_id: int
    name: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Skill(CamelCaseModel):
    """Represents a Skill from the database"""
    skill_id: int
    name: str
    description: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Partner(CamelCaseModel):
    """Represents a Partner from the database"""
    partner_id: int
    name: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ProjectRole(CamelCaseModel):
    """Represents a ProjectRole from the database"""
    student_id: int
    project_id: int
    skill_id: int
    definitive: bool
    argumentation: str | None
    drafter_id: int

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Project(CamelCaseModel):
    """Represents a Project from the database to return when a GET request happens"""
    project_id: int
    name: str
    number_of_students: int
    edition_name: str

    coaches: list[User]
    skills: list[Skill]
    partners: list[Partner]
    project_roles: list[ProjectRole]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Student(CamelCaseModel):
    """Represents a Student from the database to use in ConflictStudent"""
    student_id: int
    first_name: str
    last_name: str
    preferred_name: str
    email_address: str
    phone_number: str | None
    alumni: bool
    decision: DecisionEnum
    wants_to_be_student_coach: bool
    edition_name: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ProjectList(CamelCaseModel):
    """A list of projects"""
    projects: list[Project]


class ConflictStudent(CamelCaseModel):
    """A student together with the projects they are causing a conflict for"""
    student: Student
    projects: list[Project]


class ConflictStudentList(CamelCaseModel):
    """A list of ConflictStudents"""
    conflict_students: list[ConflictStudent]


class InputProject(BaseModel):
    """Used for passing the details of a project when creating/patching a project"""
    name: str
    number_of_students: int
    skills: list[int]
    partners: list[str]
    coaches: list[int]


# TO DO: change drafter_id to current user with authentication
class InputStudentRole(BaseModel):
    """Used for creating/patching a student role (temporary until authentication is implemented)"""
    skill_id: int
    drafter_id: int
