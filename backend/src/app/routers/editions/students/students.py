from fastapi import APIRouter

from fastapi import Depends
from src.database.database import get_session
from src.database.models import Student
from sqlalchemy.orm import Session

from typing import List

from src.app.routers.tags import Tags
from .suggestions import students_suggestions_router

students_router = APIRouter(prefix="/students", tags=[Tags.STUDENTS])
students_router.include_router(students_suggestions_router, prefix="/{student_id}")


@students_router.get("/")
async def get_students(edition_id: int, db: Session = Depends(get_session)):
    """Get a list of all students.

    Args:
        edition_id (int): The edition you want to get the students from
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        List[StudentBase]: A list of students of an edition.
    """
    return db.query(Student).all()
    #return db.query(Student).filter_by(edition_id = edition_id)



@students_router.post("/emails")
async def send_emails(edition_id: int):
    """
    Send a Yes/Maybe/No email to a list of students.
    """


@students_router.delete("/{student_id}")
async def delete_student(edition_id: int, student_id: int):
    """
    Delete all information stored about a specific student.
    """


@students_router.get("/{student_id}")
async def get_student(edition_id: int, student_id: int):
    """
    Get information about a specific student.
    """


@students_router.post("/{student_id}/decision")
async def make_decision(edition_id: int, student_id: int):
    """
    Make a finalized Yes/Maybe/No decision about a student.

    This action can only be performed by an admin.
    """


@students_router.get("/{student_id}/emails")
async def get_student_email_history(edition_id: int, student_id: int):
    """
    Get the history of all Yes/Maybe/No emails that have been sent to
    a specific student so far.
    """
