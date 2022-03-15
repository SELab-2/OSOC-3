from sqlalchemy.orm import Session

from src.database.models import Project, ProjectRole


def db_remove_student_project(db: Session, project: Project, student_id: int):
    pr = db.query(ProjectRole).where(ProjectRole.student_id == student_id and ProjectRole.project == project).one()
    db.delete(pr)
    db.commit()


def db_add_student_project(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    proj_role = ProjectRole(student_id=student_id, project_id=project.project_id, skill_id=skill_id,
                            drafter_id=drafter_id)
    db.add(proj_role)
    db.commit()


def db_change_project_role(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    pr = db.query(ProjectRole).where(ProjectRole.student_id == student_id and ProjectRole.project == project).one()
    pr.drafter_id = drafter_id
    pr.skill_id = skill_id
    db.commit()
