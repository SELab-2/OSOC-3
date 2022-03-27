import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.app.schemas.projects import ConflictStudent
from src.database.crud.projects import (db_get_all_projects, db_add_project,
                                        db_get_project, db_delete_project,
                                        db_patch_project, db_get_conflict_students)
from src.database.models import Edition, Partner, Project, User, Skill, ProjectRole, Student


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


@pytest.fixture
def current_edition(database_with_data: Session) -> Edition:
    """fixture to get the latest edition"""
    return database_with_data.query(Edition).all()[-1]


def test_get_all_projects_empty(database_session: Session):
    """test get all projects but there are none"""
    edition: Edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    projects: list[Project] = db_get_all_projects(
        database_session, edition)
    assert len(projects) == 0


def test_get_all_projects(database_with_data: Session, current_edition: Edition):
    """test get all projects"""
    projects: list[Project] = db_get_all_projects(
        database_with_data, current_edition)
    assert len(projects) == 3


def test_add_project_partner_do_not_exist_yet(database_with_data: Session, current_edition: Edition):
    """tests add a project when the project don't exist yet"""
    assert len(database_with_data.query(Partner).where(
        Partner.name == "ugent").all()) == 0
    new_project: Project = db_add_project(
        database_with_data, current_edition, "project1", 2, [1, 3], ["ugent"], [1])
    assert new_project == database_with_data.query(Project).where(
        Project.project_id == new_project.project_id).one()
    new_partner: Partner = database_with_data.query(
        Partner).where(Partner.name == "ugent").one()

    assert new_partner in new_project.partners
    assert new_project.name == "project1"
    assert new_project.edition == current_edition
    assert new_project.number_of_students == 2
    assert len(new_project.coaches) == 1
    assert new_project.coaches[0].user_id == 1
    assert len(new_project.skills) == 2
    assert new_project.skills[0].skill_id == 1
    assert new_project.skills[1].skill_id == 3


def test_add_project_partner_do_exist(database_with_data: Session, current_edition: Edition):
    """tests add a project when the project exist already """
    database_with_data.add(Partner(name="ugent"))
    assert len(database_with_data.query(Partner).where(
        Partner.name == "ugent").all()) == 1
    new_project: Project = db_add_project(
        database_with_data, current_edition, "project1", 2, [1, 3], ["ugent"], [1])
    assert new_project == database_with_data.query(Project).where(
        Project.project_id == new_project.project_id).one()
    partner: Partner = database_with_data.query(
        Partner).where(Partner.name == "ugent").one()

    assert partner in new_project.partners
    assert new_project.name == "project1"
    assert new_project.edition == current_edition
    assert new_project.number_of_students == 2
    assert len(new_project.coaches) == 1
    assert new_project.coaches[0].user_id == 1
    assert len(new_project.skills) == 2
    assert new_project.skills[0].skill_id == 1
    assert new_project.skills[1].skill_id == 3


def test_get_ghost_project(database_with_data: Session):
    """test project that don't exist"""
    with pytest.raises(NoResultFound):
        db_get_project(database_with_data, 500)


def test_get_project(database_with_data: Session):
    """test get project"""
    project: Project = db_get_project(database_with_data, 1)
    assert project.name == "project1"
    assert project.number_of_students == 2


def test_delete_project_no_project_roles(database_with_data: Session, current_edition):
    """test delete a project that don't has project roles"""
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.project_id == 3).all()) == 0
    assert len(db_get_all_projects(database_with_data, current_edition)) == 3
    db_delete_project(database_with_data, 3)
    assert len(db_get_all_projects(database_with_data, current_edition)) == 2
    assert 3 not in [project.project_id for project in db_get_all_projects(
        database_with_data, current_edition)]


def test_delete_project_with_project_roles(database_with_data: Session, current_edition):
    """test delete a project that has project roles"""
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.project_id == 1).all()) > 0
    assert len(db_get_all_projects(database_with_data, current_edition)) == 3
    db_delete_project(database_with_data, 1)
    assert len(db_get_all_projects(database_with_data, current_edition)) == 2
    assert 1 not in [project.project_id for project in db_get_all_projects(
        database_with_data, current_edition)]
    assert len(database_with_data.query(ProjectRole).where(
        ProjectRole.project_id == 1).all()) == 0


def test_patch_project(database_with_data: Session, current_edition: Edition):
    """tests patch a project"""
    assert len(database_with_data.query(Partner).where(
        Partner.name == "ugent").all()) == 0
    new_project: Project = db_add_project(
        database_with_data, current_edition, "projec1", 2, [1, 3], ["ugent"], [1])
    assert new_project == database_with_data.query(Project).where(
        Project.project_id == new_project.project_id).one()
    new_partner: Partner = database_with_data.query(
        Partner).where(Partner.name == "ugent").one()
    db_patch_project(database_with_data, new_project,
                     "project1", 2, [1, 3], ["ugent"], [1])

    assert new_partner in new_project.partners
    assert new_project.name == "project1"


def test_get_conflict_students(database_with_data: Session, current_edition: Edition):
    """test if the right ConflictStudent is given"""
    conflicts: list[ConflictStudent] = db_get_conflict_students(database_with_data, current_edition)
    assert len(conflicts) == 1
    assert conflicts[0].student.student_id == 1
    assert len(conflicts[0].projects) == 2
    assert conflicts[0].projects[0].project_id == 1
    assert conflicts[0].projects[1].project_id == 2