from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum


class Project(CamelCaseModel):
    project_id: int
    name: str
    number_of_students: int
    edition_id: int

    class Config:
        orm_mode = True


class Student(CamelCaseModel):
    student_id: int
    first_name: str
    last_name: str
    preferred_name: str
    email_address: str
    phone_number: str
    alumni: bool
    decision: DecisionEnum
    wants_to_be_student_coach: bool
    edition_id: int

    class Config:
        orm_mode = True


class ProjectList(CamelCaseModel):
    projects: list[Project]


class ConflictProject(Project):
    conflicting_students = list[Student]


class ConflictProjectList(CamelCaseModel):
    conflict_projects = list[ConflictProject]
