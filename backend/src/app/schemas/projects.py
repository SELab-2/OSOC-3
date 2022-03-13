from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum


class User(CamelCaseModel):
    user_id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class Skill(CamelCaseModel):
    skill_id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class Partner(CamelCaseModel):
    partner_id: int
    name: str

    class Config:
        orm_mode = True


class ProjectRole(CamelCaseModel):
    student_id: int
    project_id: int
    skill_id: int
    definitive: bool
    argumentation: str
    drafter_id: int

    class Config:
        orm_mode = True


class Project(CamelCaseModel):
    project_id: int
    name: str
    number_of_students: int
    edition_id: int

    coaches: list[User]
    skills: list[Skill]
    partners: list[Partner]
    project_roles: list[ProjectRole]

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
