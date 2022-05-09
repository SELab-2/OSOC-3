from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Suggestion
from src.database.enums import DecisionEnum


async def create_suggestion(db: AsyncSession, user_id: int | None, student_id: int | None,
                            decision: DecisionEnum, argumentation: str) -> Suggestion:
    """
    Create a new suggestion in the database
    """
    suggestion: Suggestion = Suggestion(
        student_id=student_id, coach_id=user_id, suggestion=decision, argumentation=argumentation)
    db.add(suggestion)
    await db.commit()
    return suggestion


async def get_suggestions_of_student(db: AsyncSession, student_id: int | None) -> list[Suggestion]:
    """Give all suggestions of a student"""
    query = select(Suggestion).where(Suggestion.student_id == student_id)
    result = await db.execute(query)
    return result.unique().scalars().all()


async def get_own_suggestion(db: AsyncSession, student_id: int | None, user_id: int | None) -> Suggestion | None:
    """Get the suggestion you made for a student"""
    # This isn't even possible but it pleases Mypy
    if student_id is None or user_id is None:
        return None

    query = select(Suggestion).where(Suggestion.student_id == student_id).where(
        Suggestion.coach_id == user_id)
    result = await db.execute(query)
    return result.unique().scalar_one_or_none()


async def get_suggestion_by_id(db: AsyncSession, suggestion_id: int) -> Suggestion:
    """Give a suggestion based on the ID"""
    result = await db.execute(select(Suggestion).where(Suggestion.suggestion_id == suggestion_id))
    return result.unique().scalar_one()


async def delete_suggestion(db: AsyncSession, suggestion: Suggestion) -> None:
    """Delete a suggestion from the database"""
    await db.delete(suggestion)
    await db.commit()


async def update_suggestion(db: AsyncSession, suggestion: Suggestion, decision: DecisionEnum,
                            argumentation: str) -> None:
    """Update a suggestion"""
    suggestion.suggestion = decision
    suggestion.argumentation = argumentation
    await db.commit()


async def get_suggestions_of_student_by_type(db: AsyncSession, student_id: int | None,
                                             type_suggestion: DecisionEnum) -> list[Suggestion]:
    """Give all suggestions of a student by type"""
    query = select(Suggestion).where(Suggestion.student_id == student_id)\
        .where(Suggestion.suggestion == type_suggestion)
    result = await db.execute(query)
    return result.unique().scalars().all()
