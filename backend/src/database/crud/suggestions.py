from sqlalchemy.orm import Session

from src.database.models import Suggestion, Student, User
from src.database.enums import DecisionEnum

def create_suggestion(db: Session, user: User, student: Student, decision: DecisionEnum, argumentation: str) -> None:
    suggestion: Suggestion = Suggestion(student=student, coach=user,suggestion=decision,argumentation=argumentation)
    db.add(suggestion)
    db.commit()

def get_suggestions_of_student(db: Session, student_id: int) -> list[Suggestion]:
    return db.query(Suggestion).where(Suggestion.student_id == student_id).all()