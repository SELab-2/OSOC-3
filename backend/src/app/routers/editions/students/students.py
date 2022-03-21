from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from starlette import status
from src.app.routers.tags import Tags
from src.app.utils.dependencies import get_student, get_edition, require_admin
from src.app.logic.students import definitive_decision_on_student
from src.database.database import get_session
from src.database.models import Student, Edition
from .suggestions import students_suggestions_router
from src.app.schemas.students import NewDecision

students_router = APIRouter(prefix="/students", tags=[Tags.STUDENTS])
students_router.include_router(
    students_suggestions_router, prefix="/{student_id}")


@students_router.get("/")
async def get_students(db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Get a list of all students.
    """
    pass


@students_router.post("/emails")
async def send_emails(edition: Edition = Depends(get_edition)):
    """
    Send a Yes/Maybe/No email to a list of students.
    """
    pass


@students_router.delete("/{student_id}")
async def delete_student(edition: Edition = Depends(get_edition), student: Student = Depends(get_student)):
    """
    Delete all information stored about a specific student.
    """
    pass


@students_router.get("/{student_id}")
async def get_student_by_id(edition: Edition = Depends(get_edition), student: Student = Depends(get_student)):
    """
    Get information about a specific student.
    """
    pass


@students_router.put("/{student_id}/decision", dependencies=[Depends(require_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def make_decision(decision: NewDecision,student: Student = Depends(get_student), db: Session = Depends(get_session)) -> None:
    """
    Make a finalized Yes/Maybe/No decision about a student.

    This action can only be performed by an admin.
    """
    definitive_decision_on_student(db,student,decision)


@students_router.get("/{student_id}/emails")
async def get_student_email_history(edition: Edition = Depends(get_edition), student: Student = Depends(get_student)):
    """
    Get the history of all Yes/Maybe/No emails that have been sent to
    a specific student so far.
    """
    pass
