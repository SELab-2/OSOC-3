from sqlalchemy.orm import Session

from src.database.models import Suggestion
from src.database.enums import DecisionEnum


def create_suggestion(db: Session, user_id: int | None, student_id: int | None,
                      decision: DecisionEnum, argumentation: str) -> Suggestion:
    """
    Create a new suggestion in the database
    """
    suggestion: Suggestion = Suggestion(
        student_id=student_id, coach_id=user_id, suggestion=decision, argumentation=argumentation)
    db.add(suggestion)
    db.commit()
    return suggestion


def get_suggestions_of_student(db: Session, student_id: int | None) -> list[Suggestion]:
    """Give all suggestions of a student"""
    return db.query(Suggestion).where(Suggestion.student_id == student_id).all()


def get_suggestion_by_id(db: Session, suggestion_id: int) -> Suggestion:
    """Give a suggestion based on the ID"""
    return db.query(Suggestion).where(Suggestion.suggestion_id == suggestion_id).one()


def delete_suggestion(db: Session, suggestion: Suggestion) -> None:
    """Delete a suggestion from the database"""
    db.delete(suggestion)


def update_suggestion(db: Session, suggestion: Suggestion, decision: DecisionEnum, argumentation: str) -> None:
    """Update a suggestion"""
    suggestion.suggestion = decision
    suggestion.argumentation = argumentation
    db.commit()


def get_suggestions_of_student_by_type(db: Session, student_id: int | None, type: DecisionEnum) -> list[Suggestion]:
    """Give all suggestions of a student by type"""
    return db.query(Suggestion).where(Suggestion.student_id == student_id).where(Suggestion.suggestion == type).all()
