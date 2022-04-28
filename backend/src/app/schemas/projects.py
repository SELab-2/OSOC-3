from dataclasses import dataclass
from pydantic import BaseModel

from src.app.schemas.utils import CamelCaseModel


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

    coaches: list[User]
    skills: list[Skill]
    partners: list[Partner]
    project_roles: list[ProjectRole]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Student(CamelCaseModel):
    """Represents a Student to use in ConflictStudent"""
    student_id: int
    first_name: str
    last_name: str

    class Config:
        """Config Class"""
        orm_mode = True


class ConflictProject(CamelCaseModel):
    """A project to be used in ConflictStudent"""
    project_id: int
    name: str

    class Config:
        """Config Class"""
        orm_mode = True


class ProjectList(CamelCaseModel):
    """A list of projects"""
    projects: list[Project]


class ConflictStudent(CamelCaseModel):
    """A student together with the projects they are causing a conflict for"""
    student: Student
    projects: list[ConflictProject]

    class Config:
        """Config Class"""
        orm_mode = True


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


class InputStudentRole(BaseModel):
    """Used for creating/patching a student role"""
    skill_id: int


@dataclass
class QueryParamsProjects:
    """search query parameters for projects"""
    name: str = ""
    coach: bool = False
    page: int = 0
