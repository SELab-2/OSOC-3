import pytest
from sqlalchemy.orm import Session
from tests.fill_database import fill_database
from src.database.models import Student
from src.database.crud.students import get_student_by_id
from sqlalchemy.orm.exc import NoResultFound

def test_get_student_by_id(database_session: Session):
    fill_database(database_session)
    student: Student = get_student_by_id(database_session, 1)
    assert student.first_name == "Jos"
    assert student.last_name == "Vermeulen"
    assert student.student_id == 1
    assert student.email_address == "josvermeulen@mail.com"

def test_no_student(database_session: Session):
    with pytest.raises(NoResultFound):
        get_student_by_id(database_session, 5)