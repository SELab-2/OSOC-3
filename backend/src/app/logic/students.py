from sqlalchemy.orm import Session

from src.app.schemas.students import NewDecision
from src.database.crud.students import set_definitive_decision_on_student, delete_student
from src.database.models import Student
#from src.app.schemas.suggestion import SuggestionListResponse, SuggestionResponse

def definitive_decision_on_student(db: Session, student: Student, decision: NewDecision):
    """Set a definitive decion on a student"""
    set_definitive_decision_on_student(db, student, decision.decision)


def remove_student(db: Session, student: Student):
    """delete a student"""
    delete_student(db, student)
