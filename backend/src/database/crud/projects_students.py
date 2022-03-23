from sqlalchemy.orm import Session

from src.database.models import Project, ProjectRole


def db_remove_student_project(db: Session, project: Project, student_id: int):
    """Remove a student from a project in the database"""
    proj_role = db.query(ProjectRole).where(ProjectRole.student_id ==
                                     student_id).where(ProjectRole.project == project).one()
    db.delete(proj_role)
    db.commit()


def db_add_student_project(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Add a student to a project in the database"""
    proj_role = ProjectRole(student_id=student_id, project_id=project.project_id, skill_id=skill_id,
                            drafter_id=drafter_id)
    db.add(proj_role)
    db.commit()


def db_change_project_role(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Change the role of a student in a project and update the drafter"""
    proj_role = db.query(ProjectRole).where(
        ProjectRole.student_id == student_id).where(ProjectRole.project == project).one()
    proj_role.drafter_id = drafter_id
    proj_role.skill_id = skill_id
    db.commit()
