from sqlalchemy.orm import Session

from src.app.schemas.projects import ProjectList, Project, ConflictStudentList, Student, ConflictStudent
from src.database.crud.projects import db_get_all_projects, db_add_project, db_delete_project, \
    db_patch_project, db_get_conflict_students
from src.database.models import Edition


def logic_get_project_list(db: Session, edition: Edition) -> ProjectList:
    """Returns a list of all projects from a certain edition"""
    db_all_projects = db_get_all_projects(db, edition)
    projects_model = []
    for project in db_all_projects:
        project_model = Project(project_id=project.project_id, name=project.name,
                                number_of_students=project.number_of_students,
                                edition_name=project.edition.name, coaches=project.coaches, skills=project.skills,
                                partners=project.partners, project_roles=project.project_roles)
        projects_model.append(project_model)
    return ProjectList(projects=projects_model)


def logic_create_project(db: Session, edition: Edition, name: str, number_of_students: int, skills: list[int],
                         partners: list[str], coaches: list[int]) -> Project:
    """Create a new project"""
    project = db_add_project(db, edition, name, number_of_students, skills, partners, coaches)
    return Project(project_id=project.project_id, name=project.name, number_of_students=project.number_of_students,
                   edition_name=project.edition.name, coaches=project.coaches, skills=project.skills,
                   partners=project.partners, project_roles=project.project_roles)


def logic_delete_project(db: Session, project_id: int):
    """Delete a project"""
    db_delete_project(db, project_id)


def logic_patch_project(db: Session, project_id: int, name: str, number_of_students: int,
                        skills: list[int],
                        partners: list[str], coaches: list[int]):
    """Make changes to a project"""
    db_patch_project(db, project_id, name, number_of_students, skills, partners, coaches)


def logic_get_conflicts(db: Session, edition: Edition) -> ConflictStudentList:
    """Returns a list of all students together with the projects they are causing a conflict for"""
    conflicts = db_get_conflict_students(db, edition)
    conflicts_model = []
    for student, projects in conflicts:
        student_model = Student(student_id=student.student_id,
                                first_name=student.first_name,
                                last_name=student.last_name,
                                preferred_name=student.preferred_name,
                                email_address=student.email_address,
                                phone_number=student.phone_number,
                                alumni=student.alumni,
                                decision=student.decision,
                                wants_to_be_student_coach=student.wants_to_be_student_coach,
                                edition_name=edition.name)
        projects_model = []
        for project in projects:
            project_model = Project(project_id=project.project_id, name=project.name,
                                    number_of_students=project.number_of_students,
                                    edition_name=edition.name, coaches=project.coaches, skills=project.skills,
                                    partners=project.partners, project_roles=project.project_roles)
            projects_model.append(project_model)

        conflicts_model.append(ConflictStudent(student=student_model, projects=projects_model))

    return ConflictStudentList(conflict_students=conflicts_model)
