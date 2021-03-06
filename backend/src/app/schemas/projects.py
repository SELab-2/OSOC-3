from dataclasses import dataclass

from pydantic import BaseModel, validator

from src.app.schemas.skills import Skill
from src.app.schemas.utils import CamelCaseModel
from src.app.schemas.validators import validate_url


class User(CamelCaseModel):
    """Represents a User from the database"""
    user_id: int
    name: str

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


class Student(CamelCaseModel):
    """Represents a Partner from the database"""
    student_id: int
    first_name: str
    last_name: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ProjectRoleSuggestion(CamelCaseModel):
    """Represents a ProjectRole from the database"""
    project_role_suggestion_id: int
    argumentation: str | None
    drafter: User | None
    student: Student | None

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ReturnProjectRoleSuggestion(CamelCaseModel):
    """return a project role suggestion"""
    project_role_suggestion: ProjectRoleSuggestion


class ProjectRole(CamelCaseModel):
    """Represents a ProjectRole from the database"""
    project_role_id: int
    project_id: int
    description: str | None
    skill: Skill
    slots: int

    suggestions: list[ProjectRoleSuggestion]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ProjectRoleResponseList(CamelCaseModel):
    """Response list containing project roles"""
    project_roles: list[ProjectRole]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Project(CamelCaseModel):
    """Represents a Project from the database to return when a GET request happens"""
    project_id: int
    name: str
    info_url: str | None

    coaches: list[User]
    partners: list[Partner]
    project_roles: list[ProjectRole]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ProjectList(CamelCaseModel):
    """A list of projects"""
    projects: list[Project]


class ConflictProject(CamelCaseModel):
    """A project to be used in ConflictStudent"""
    project_id: int
    name: str
    info_url: str | None

    class Config:
        """Config Class"""
        orm_mode = True


class ConflictProjectRole(CamelCaseModel):
    """A project to be used in ConflictStudent"""
    project_role_id: int
    project: ConflictProject

    class Config:
        """Config Class"""
        orm_mode = True


class ConflictRoleSuggestion(CamelCaseModel):
    """Represents a ProjectRole from the database"""
    project_role_suggestion_id: int
    project_role: ConflictProjectRole

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class ConflictStudent(CamelCaseModel):
    """A student together with the projects they are causing a conflict for"""
    student_id: int
    first_name: str
    last_name: str
    pr_suggestions: list[ConflictRoleSuggestion]

    class Config:
        """Config Class"""
        orm_mode = True


class ConflictStudentList(CamelCaseModel):
    """A list of ConflictStudents"""
    conflict_students: list[ConflictStudent]


class InputProjectRole(BaseModel):
    """Used for creating a project role"""
    skill_id: int
    description: str | None
    slots: int


class InputProject(BaseModel):
    """Used for passing the details of a project when creating/patching a project"""
    name: str
    info_url: str | None
    partners: list[str]
    coaches: list[int]

    @validator('info_url')
    @classmethod
    def is_url(cls, info_url: str | None):
        """Validate url"""
        return validate_url(info_url)


class InputArgumentation(BaseModel):
    """Used for creating/patching a student role"""
    argumentation: str | None


@dataclass
class QueryParamsProjects:
    """search query parameters for projects"""
    name: str = ""
    coach: bool = False
    page: int = 0
