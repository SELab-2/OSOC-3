from sqlalchemy.orm import Session

import src.app.logic.projects as logic_projects
import src.database.crud.projects_students as crud
from src.app.exceptions.projects import StudentInConflictException, FailedToAddProjectRoleException
from src.app.schemas.projects import ConflictStudentList
from src.database.models import Project, ProjectRole, Student, Skill


def remove_student_project(db: Session, project: Project, student_id: int):
    """Remove a student from a project"""
    crud.remove_student_project(db, project, student_id)


def add_student_project(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
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

    crud.add_student_project(db, project, student_id, skill_id, drafter_id)


def change_project_role(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
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

    crud.change_project_role(db, project, student_id, skill_id, drafter_id)


def confirm_project_role(db: Session, project: Project, student_id: int):
    """Definitively bind this student to the project"""
    # check if there are any conflicts concerning this student
    conflict_list: ConflictStudentList = logic_projects.get_conflicts(db, project.edition)
    for conflict in conflict_list.conflict_students:
        if conflict.student.student_id == student_id:
            raise StudentInConflictException

    crud.confirm_project_role(db, project, student_id)
