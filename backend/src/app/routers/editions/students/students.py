from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.logic.students import (
    definitive_decision_on_student, remove_student, get_student_return,
    get_students_search, get_emails_of_student, make_new_email,
    last_emails_of_students)
from src.app.routers.tags import Tags
from src.app.schemas.students import (NewDecision, CommonQueryParams, ReturnStudent, ReturnStudentList,
                                      ReturnStudentMailList, NewEmail, EmailsSearchQueryParams,
                                      ListReturnStudentMailList)
from src.app.utils.dependencies import get_student, get_edition, require_admin, require_auth
from src.database.database import get_session
from src.database.models import Student, Edition
from .suggestions import students_suggestions_router

students_router = APIRouter(prefix="/students", tags=[Tags.STUDENTS])
students_router.include_router(
    students_suggestions_router, prefix="/{student_id}")


@students_router.get("", dependencies=[Depends(require_auth)], response_model=ReturnStudentList)
async def get_students(db: AsyncSession = Depends(get_session),
                       commons: CommonQueryParams = Depends(CommonQueryParams),
                       edition: Edition = Depends(get_edition)):
    """
    Get a list of all students.
    """
    return await get_students_search(db, edition, commons)


@students_router.post("/emails", dependencies=[Depends(require_admin)],
                      status_code=status.HTTP_201_CREATED, response_model=ListReturnStudentMailList)
async def send_emails(new_email: NewEmail, db: AsyncSession = Depends(get_session),
                      edition: Edition = Depends(get_edition)):
    """
    Send a email to a list of students.
    """
    return await make_new_email(db, edition, new_email)


@students_router.get("/emails", dependencies=[Depends(require_admin)],
                     response_model=ListReturnStudentMailList)
async def get_emails(db: AsyncSession = Depends(get_session), edition: Edition = Depends(get_edition),
                     commons: EmailsSearchQueryParams = Depends(EmailsSearchQueryParams)):
    """
    Get last emails of students
    """
    return await last_emails_of_students(db, edition, commons)


@students_router.delete("/{student_id}", dependencies=[Depends(require_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student: Student = Depends(get_student), db: AsyncSession = Depends(get_session)):
    """
    Delete all information stored about a specific student.
    """
    await remove_student(db, student)


@students_router.get("/{student_id}", dependencies=[Depends(require_auth)], response_model=ReturnStudent)
async def get_student_by_id(edition: Edition = Depends(get_edition), student: Student = Depends(get_student)):
    """
    Get information about a specific student.
    """
    return get_student_return(student, edition)


@students_router.put("/{student_id}/decision", dependencies=[Depends(require_admin)],
                     status_code=status.HTTP_204_NO_CONTENT)
async def make_decision(decision: NewDecision, student: Student = Depends(get_student),
                        db: AsyncSession = Depends(get_session)):
    """
    Make a finalized Yes/Maybe/No decision about a student.

    This action can only be performed by an admin.
    """
    await definitive_decision_on_student(db, student, decision)


@students_router.get("/{student_id}/emails", dependencies=[Depends(require_admin)],
                     response_model=ReturnStudentMailList)
async def get_student_email_history(edition: Edition = Depends(get_edition), student: Student = Depends(get_student),
                                    db: AsyncSession = Depends(get_session)):
    """
    Get the history of all Yes/Maybe/No emails that have been sent to
    a specific student so far.
    """
    return await get_emails_of_student(db, edition, student)
