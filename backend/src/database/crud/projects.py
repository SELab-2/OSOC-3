from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.app.schemas.projects import ConflictStudent
from src.database.models import Project, Edition, Student, ProjectRole, Skill, User, Partner


def db_get_all_projects(db: Session, edition: Edition) -> list[Project]:
    return db.query(Project).where(Project.edition == edition).all()


def db_add_project(db: Session, edition: Edition, name: str, number_of_students: int, skills: [int],
                   partners: [str], coaches: [int]):
    skills_obj = [db.query(Skill).where(Skill.skill_id == skill).one() for skill in skills]
    coaches_obj = [db.query(User).where(User.user_id) == coach for coach in coaches]
    partners_obj = []
    for partner in partners:
        try:
            partners_obj.append(db.query(Partner).where(Partner.name == partner).one())
        except NoResultFound:
            partner_obj = Partner(name=partner)
            db.add(partner_obj)
            partners_obj.append(partner_obj)
    project = Project(name=name, number_of_students=number_of_students, edition_id=edition.edition_id,
                      skills=skills_obj, coaches=coaches_obj, partners=partners_obj)

    db.add(project)
    db.commit()


def db_get_project(db: Session, project_id: int) -> Project:
    return db.query(Project).where(Project.project_id == project_id).one()


def db_delete_project(db: Session, project_id: int):
    proj_roles = db.query(ProjectRole).where(ProjectRole.project_id == project_id).all()
    for pr in proj_roles:
        db.delete(pr)

    project = db_get_project(db, project_id)
    db.delete(project)
    db.commit()


def db_patch_project(db: Session, project: Project, name: str, number_of_students: int, skills: [int],
                     partners: [str], coaches: [int]):
    skills_obj = [db.query(Skill).where(Skill.skill_id == skill).one() for skill in skills]
    coaches_obj = [db.query(User).where(User.user_id) == coach for coach in coaches]
    partners_obj = []
    for partner in partners:
        try:
            partners_obj.append(db.query(Partner).where(Partner.name == partner).one())
        except NoResultFound:
            partner_obj = Partner(name=partner)
            db.add(partner_obj)
            partners_obj.append(partner_obj)

    project.name = name
    project.number_of_students = number_of_students
    project.skills = skills_obj
    project.coaches = coaches_obj
    project.partners = partners_obj
    db.commit()


# def db_get_conflict_students(db: Session, edition: Edition) -> list[Student]:
#     students = db.query(Student).where(Student.edition == edition).all()
#     conflicts = []
#     for s in students:
#         if len(s.project_roles) > 1:
#             conflicts.append(s)
#     return conflicts


def db_get_conflict_students(db: Session, edition: Edition) -> list[ConflictStudent]:

    students = db.query(Student).where(Student.edition == edition).all()
    conflict_students = []
    projs = []
    for student in students:
        if len(student.project_roles) > 1:
            proj_ids = db.query(ProjectRole.project_id).where(ProjectRole.student_id == student.student_id).all()
            for proj_id in proj_ids:
                proj_id = proj_id[0]
                proj = db.query(Project).where(Project.project_id == proj_id).one()
                projs.append(proj)
            cp = ConflictStudent(student=student, projects=projs)
            conflict_students.append(cp)
    return conflict_students

