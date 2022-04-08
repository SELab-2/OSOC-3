from sqlalchemy.orm import Session

from src.database.models import Project, ProjectRole, Skill, User, Student


def db_remove_student_project(db: Session, project: Project, student_id: int):
    """Remove a student from a project in the database"""
    proj_role = db.query(ProjectRole).where(ProjectRole.student_id ==
                                            student_id).where(ProjectRole.project == project).one()
    db.delete(proj_role)
    db.commit()


def db_add_student_project(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Add a student to a project in the database"""

    # check if all parameters exist in the database
    db.query(Skill).where(Skill.skill_id == skill_id).one()
    db.query(User).where(User.user_id == drafter_id).one()
    db.query(Student).where(Student.student_id == student_id).one()

    proj_role = ProjectRole(student_id=student_id, project_id=project.project_id, skill_id=skill_id,
                            drafter_id=drafter_id)
    db.add(proj_role)
    db.commit()


def db_change_project_role(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Change the role of a student in a project and update the drafter"""

    # check if all parameters exist in the database
    db.query(Skill).where(Skill.skill_id == skill_id).one()
    db.query(User).where(User.user_id == drafter_id).one()
    db.query(Student).where(Student.student_id == student_id).one()

    proj_role = db.query(ProjectRole).where(
        ProjectRole.student_id == student_id).where(ProjectRole.project == project).one()
    proj_role.drafter_id = drafter_id
    proj_role.skill_id = skill_id
    db.commit()


def db_confirm_project_role(db: Session, project: Project, student_id: int):
    proj_role = db.query(ProjectRole).where(ProjectRole.student_id == student_id) \
        .where(ProjectRole.project == project).one()

    proj_role.definitive = True
    db.commit()
