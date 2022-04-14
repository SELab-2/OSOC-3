from sqlalchemy.orm import Session
from src.app.exceptions.projects import StudentInConflictException, FailedToAddProjectRoleException
from src.app.logic.projects import logic_get_conflicts
from src.app.schemas.projects import ConflictStudentList

from src.database.crud.projects_students import db_remove_student_project, db_add_student_project, \
    db_change_project_role, db_confirm_project_role
from src.database.models import Project, ProjectRole, Student, Skill


def logic_remove_student_project(db: Session, project: Project, student_id: int):
    """Remove a student from a project"""
    db_remove_student_project(db, project, student_id)


def logic_add_student_project(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Add a student to a project"""
    # check this project-skill combination does not exist yet
    if db.query(ProjectRole).where(ProjectRole.skill_id == skill_id).where(ProjectRole.project == project) \
            .count() > 0:
        raise FailedToAddProjectRoleException
    # check that the student has the skill
    student = db.query(Student).where(Student.student_id == student_id).one()
    skill = db.query(Skill).where(Skill.skill_id == skill_id).one()
    if skill not in student.skills:
        raise FailedToAddProjectRoleException
    # check that the student has not been confirmed in another project yet
    if db.query(ProjectRole).where(ProjectRole.student == student).where(ProjectRole.definitive.is_(True)).count() > 0:
        raise FailedToAddProjectRoleException
    # check that the project requires the skill
    project = db.query(Project).where(Project.project_id == project.project_id).one()
    if skill not in project.skills:
        raise FailedToAddProjectRoleException

    db_add_student_project(db, project, student_id, skill_id, drafter_id)


def logic_change_project_role(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Change the role of the student in the project"""
    # check this project-skill combination does not exist yet
    if db.query(ProjectRole).where(ProjectRole.skill_id == skill_id).where(ProjectRole.project == project) \
            .count() > 0:
        raise FailedToAddProjectRoleException
    # check that the student has the skill
    student = db.query(Student).where(Student.student_id == student_id).one()
    skill = db.query(Skill).where(Skill.skill_id == skill_id).one()
    if skill not in student.skills:
        raise FailedToAddProjectRoleException
    # check that the student has not been confirmed in another project yet
    if db.query(ProjectRole).where(ProjectRole.student == student).where(
            ProjectRole.definitive.is_(True)).count() > 0:
        raise FailedToAddProjectRoleException
    # check that the project requires the skill
    project = db.query(Project).where(Project.project_id == project.project_id).one()
    if skill not in project.skills:
        raise FailedToAddProjectRoleException

    db_change_project_role(db, project, student_id, skill_id, drafter_id)


def logic_confirm_project_role(db: Session, project: Project, student_id: int):
    """Definitively bind this student to the project"""
    # check if there are any conflicts concerning this student
    conflict_list: ConflictStudentList = logic_get_conflicts(db, project.edition)
    for conflict in conflict_list.conflict_students:
        if conflict.student.student_id == student_id:
            raise StudentInConflictException

    db_confirm_project_role(db, project, student_id)
