from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, Query

from src.app.schemas.projects import InputProject, QueryParamsProjects
from src.database.crud.util import paginate
from src.database.models import Project, Edition, Student, ProjectRole, Skill, User, Partner


def _get_projects_for_edition_query(db: Session, edition: Edition) -> Query:
    return db.query(Project).where(Project.edition == edition).order_by(Project.project_id)


def get_projects_for_edition(db: Session, edition: Edition) -> list[Project]:
    """Returns a list of all projects from a certain edition from the database"""
    return _get_projects_for_edition_query(db, edition).all()


def get_projects_for_edition_page(db: Session, edition: Edition,
                                  search_params: QueryParamsProjects, user: User) -> list[Project]:
    """Returns a paginated list of all projects from a certain edition from the database"""
    query = _get_projects_for_edition_query(db, edition).where(
        Project.name.contains(search_params.name))
    if search_params.coach:
        query = query.where(Project.project_id.in_([user_project.project_id for user_project in user.projects]))
    projects: list[Project] = paginate(query, search_params.page).all()

    return projects


def add_project(db: Session, edition: Edition, input_project: InputProject) -> Project:
    """
    Add a project to the database
    If there are partner names that are not already in the database, add them
    """
    skills_obj = [db.query(Skill).where(Skill.skill_id == skill).one()
                  for skill in input_project.skills]
    coaches_obj = [db.query(User).where(User.user_id == coach).one()
                   for coach in input_project.coaches]
    partners_obj = []
    for partner in input_project.partners:
        try:
            partners_obj.append(db.query(Partner).where(
                Partner.name == partner).one())
        except NoResultFound:
            partner_obj = Partner(name=partner)
            db.add(partner_obj)
            partners_obj.append(partner_obj)
    project = Project(name=input_project.name, number_of_students=input_project.number_of_students,
                      edition_id=edition.edition_id, skills=skills_obj, coaches=coaches_obj, partners=partners_obj)

    db.add(project)
    db.commit()
    return project


def get_project(db: Session, project_id: int) -> Project:
    """Query a specific project from the database through its ID"""
    return db.query(Project).where(Project.project_id == project_id).one()


def delete_project(db: Session, project_id: int):
    """Delete a specific project from the database"""
    proj_roles = db.query(ProjectRole).where(
        ProjectRole.project_id == project_id).all()
    for proj_role in proj_roles:
        db.delete(proj_role)

    project = get_project(db, project_id)
    db.delete(project)
    db.commit()


def patch_project(db: Session, project_id: int, input_project: InputProject):
    """
    Change some fields of a Project in the database
    If there are partner names that are not already in the database, add them
    """
    project = db.query(Project).where(Project.project_id == project_id).one()

    skills_obj = [db.query(Skill).where(Skill.skill_id == skill).one()
                  for skill in input_project.skills]
    coaches_obj = [db.query(User).where(User.user_id == coach).one()
                   for coach in input_project.coaches]
    partners_obj = []
    for partner in input_project.partners:
        try:
            partners_obj.append(db.query(Partner).where(
                Partner.name == partner).one())
        except NoResultFound:
            partner_obj = Partner(name=partner)
            db.add(partner_obj)
            partners_obj.append(partner_obj)

    project.name = input_project.name
    project.number_of_students = input_project.number_of_students
    project.skills = skills_obj
    project.coaches = coaches_obj
    project.partners = partners_obj
    db.commit()


def get_conflict_students(db: Session, edition: Edition) -> list[tuple[Student, list[Project]]]:
    """
    Query all students that are causing conflicts for a certain edition
    Return a ConflictStudent for each student that causes a conflict
    This class contains a student together with all projects they are causing a conflict for
    """
    students = db.query(Student).where(Student.edition == edition).all()
    conflict_students = []
    projs = []
    for student in students:
        if len(student.project_roles) > 1:
            proj_ids = db.query(ProjectRole.project_id).where(
                ProjectRole.student_id == student.student_id).all()
            for proj_id in proj_ids:
                proj_id = proj_id[0]
                proj = db.query(Project).where(
                    Project.project_id == proj_id).one()
                projs.append(proj)
            conflict_student = (student, projs)
            conflict_students.append(conflict_student)
    return conflict_students
