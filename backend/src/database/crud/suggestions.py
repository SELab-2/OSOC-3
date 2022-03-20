from sqlalchemy.orm import Session

from src.database.models import Suggestion, Student, User
from src.database.enums import DecisionEnum

def create_suggestion(db: Session, user_id: int, student_id: int, decision: DecisionEnum, argumentation: str) -> Suggestion:
    suggestion: Suggestion = Suggestion(student_id=student_id, coach_id=user_id,suggestion=decision,argumentation=argumentation)
    db.add(suggestion)
    db.commit()
    return suggestion

def get_suggestions_of_student(db: Session, student_id: int) -> list[Suggestion]:
    return db.query(Suggestion).where(Suggestion.student_id == student_id).all()

def get_suggestion_by_id(db: Session, suggestion_id:int) -> Suggestion:
    return db.query(Suggestion).where(Suggestion.suggestion_id == suggestion_id).one()

def delete_suggestion(db: Session, suggestion: Suggestion) -> None:
    db.delete(suggestion)

def update_suggestion(db: Session, suggestion: Suggestion, decision: DecisionEnum, argumentation: str) -> None:
    suggestion.suggestion = decision
    suggestion.argumentation = argumentation
    db.commit()