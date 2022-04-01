from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum


class NewDecision(CamelCaseModel):
    """the fields of a decision"""
    decision: DecisionEnum


class Student(CamelCaseModel):
    """
    Model to represent a Coach
    Sent as a response to API /GET requests
    """
    student_id: int
    first_name: str
    last_name: str
    preferred_name: str
    email_address: str
    phone_number: str
    alumni: bool
    # cv_url = Column(Text)
    decision: DecisionEnum
    wants_to_be_student_coach: bool
    edition_id: int

    class Config:
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
                 student_coach: bool = False, skill_ids: list[int] = None) -> None:
        """init"""
        self.first_name = first_name
        self.last_name = last_name
        self.alumni = alumni
        self.student_coach = student_coach
        self.skill_ids = skill_ids
