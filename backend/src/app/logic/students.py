from sqlalchemy.orm import Session

from src.app.schemas.students import NewDecision
from src.database.crud.students import set_definitive_decision_on_student
from src.database.models import Suggestion, User, Student
#from src.app.schemas.suggestion import SuggestionListResponse, SuggestionResponse
from src.app.exceptions.authentication import MissingPermissionsException

def definitive_decision_on_student(db: Session, student: Student, decision: NewDecision):
    set_definitive_decision_on_student(db, student, decision.decision)