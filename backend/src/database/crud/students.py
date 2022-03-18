from sqlalchemy.orm import Session
from src.database.models import Student

def get_student_by_id(database_session: Session, student_id: int) -> Student:
    return database_session.query(Student).where(Student.student_id == student_id).one()
