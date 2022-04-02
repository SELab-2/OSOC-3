import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.database.crud.projects_students import (
    db_remove_student_project, db_add_student_project, db_change_project_role)
from src.database.models import Edition, Project, User, Skill, ProjectRole, Student


@pytest.fixture
def database_with_data(database_session: Session) -> Session:
    """fixture for adding data to the database"""
    edition: Edition = Edition(year=2022)
    database_session.add(edition)
    project1 = Project(name="project1", edition=edition, number_of_students=2)
    project2 = Project(name="project2", edition=edition, number_of_students=3)
    project3 = Project(name="project3", edition=edition, number_of_students=3)
    database_session.add(project1)
    database_session.add(project2)
    database_session.add(project3)
    user: User = User(name="coach1")
    database_session.add(user)
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3])
    student02: Student = Student(first_name="Isabella", last_name="Christensen", preferred_name="Isabella",
                                 email_address="isabella.christensen@example.com", phone_number="98389723", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2])
    project_role1: ProjectRole = ProjectRole(
        student=student01, project=project1, skill=skill1, drafter=user, argumentation="argmunet")
    project_role2: ProjectRole = ProjectRole(
        student=student01, project=project2, skill=skill3, drafter=user, argumentation="argmunet")
    project_role3: ProjectRole = ProjectRole(
        student=student02, project=project1, skill=skill1, drafter=user, argumentation="argmunet")
    database_session.add(project_role1)
    database_session.add(project_role2)
    database_session.add(project_role3)
    database_session.commit()

    return database_session


def test_remove_student_from_project(database_with_data: Session):
    """test removing a student form a project"""
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.student_id == 1).all()) == 2
    project: Project = database_with_data.query(
        Project).where(Project.project_id == 1).one()
    db_remove_student_project(database_with_data, project, 1)
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.student_id == 1).all()) == 1


def test_remove_student_from_project_not_assigned_to(database_with_data: Session):
    """test removing a student form a project that don't exist"""
    project: Project = database_with_data.query(
        Project).where(Project.project_id == 2).one()
    with pytest.raises(NoResultFound):
        db_remove_student_project(database_with_data, project, 2)


def test_add_student_project(database_with_data: Session):
    """tests add student to a project"""
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.student_id == 2).all()) == 1
    project: Project = database_with_data.query(
        Project).where(Project.project_id == 2).one()
    db_add_student_project(database_with_data, project, 2, 2, 1)
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.student_id == 2).all()) == 2


def test_change_project_role(database_with_data: Session):
    """test change project role"""
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.student_id == 2).all()) == 1
    project: Project = database_with_data.query(
        Project).where(Project.project_id == 1).one()
    project_role: ProjectRole = database_with_data.query(ProjectRole).where(
        ProjectRole.project_id == 1).where(ProjectRole.student_id == 2).one()
    assert project_role.skill_id == 1
    db_change_project_role(database_with_data, project, 2, 2, 1)
    assert project_role.skill_id == 2

def test_change_project_role_not_assigned_to(database_with_data: Session):
    """test change project role"""
    project: Project = database_with_data.query(
        Project).where(Project.project_id == 2).one()
    with pytest.raises(NoResultFound):
        db_change_project_role(database_with_data, project, 2, 2, 1)
