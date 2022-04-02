import pytest
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Edition, Project, User, Skill, ProjectRole, Student, Partner
from tests.utils.authorization import AuthClient


@pytest.fixture
def database_with_data(database_session: Session) -> Session:
    """fixture for adding data to the database"""
    edition: Edition = Edition(year=2022, name="ed2022")
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


def test_get_projects(database_with_data: Session, auth_client: AuthClient):
    """Tests get all projects"""
    auth_client.admin()
    response = auth_client.get("/editions/ed2022/projects")
    json = response.json()

    assert len(json['projects']) == 3
    assert json['projects'][0]['name'] == "project1"
    assert json['projects'][1]['name'] == "project2"
    assert json['projects'][2]['name'] == "project3"


def test_get_project(database_with_data: Session, auth_client: AuthClient):
    """Tests get a specific project"""
    auth_client.admin()
    response = auth_client.get("/editions/ed2022/projects/1")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['name'] == 'project1'


def test_delete_project(database_with_data: Session, auth_client: AuthClient):
    """Tests delete a project"""
    auth_client.admin()
    response = auth_client.get("/editions/ed2022/projects/1")
    assert response.status_code == status.HTTP_200_OK
    response = auth_client.delete("/editions/ed2022/projects/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = auth_client.get("/editions/ed2022/projects/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_ghost_project(database_with_data: Session, auth_client: AuthClient):
    """Tests delete a project that doesn't exist"""
    auth_client.admin()
    response = auth_client.get("/editions/ed2022/projects/400")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = auth_client.delete("/editions/ed2022/projects/400")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_project(database_with_data: Session, auth_client: AuthClient):
    """Tests creating a project"""
    auth_client.admin()
    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()
    assert len(json['projects']) == 3
    assert len(database_with_data.query(Partner).all()) == 0

    response = \
        auth_client.post("/editions/ed2022/projects/",
                         json={"name": "test",
                               "number_of_students": 5,
                               "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [1]})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == 'test'
    assert response.json()["partners"][0]["name"] == "ugent"

    assert len(database_with_data.query(Partner).all()) == 1

    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()

    assert len(json['projects']) == 4
    assert json['projects'][3]['name'] == "test"


def test_create_project_same_partner(database_with_data: Session, auth_client: AuthClient):
    """Tests that creating a project doesn't create a partner if the partner already exists"""
    auth_client.admin()
    assert len(database_with_data.query(Partner).all()) == 0

    auth_client.post("/editions/ed2022/projects/",
                     json={"name": "test1",
                           "number_of_students": 2,
                           "skills": [1, 2], "partners": ["ugent"], "coaches": [1]})
    auth_client.post("/editions/ed2022/projects/",
                     json={"name": "test2",
                           "number_of_students": 2,
                           "skills": [1, 2], "partners": ["ugent"], "coaches": [1]})
    assert len(database_with_data.query(Partner).all()) == 1


def test_create_project_non_existing_skills(database_with_data: Session, auth_client: AuthClient):
    """Tests creating a project with non-existing skills"""
    auth_client.admin()
    response = auth_client.get('/editions/ed2022/projects')

    json = response.json()
    assert len(json['projects']) == 3

    assert len(database_with_data.query(Skill).where(
        Skill.skill_id == 100).all()) == 0

    response = auth_client.post("/editions/ed2022/projects/",
                                json={"name": "test1",
                                      "number_of_students": 1,
                                      "skills": [100], "partners": ["ugent"], "coaches": [1]})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()
    assert len(json['projects']) == 3


def test_create_project_non_existing_coach(database_with_data: Session, auth_client: AuthClient):
    """Tests creating a project with a coach that doesn't exist"""
    auth_client.admin()
    response = auth_client.get('/editions/ed2022/projects')

    json = response.json()
    assert len(json['projects']) == 3

    assert len(database_with_data.query(Student).where(
        Student.edition_id == 10).all()) == 0

    response = auth_client.post("/editions/ed2022/projects/",
                                json={"name": "test2",
                                      "number_of_students": 1,
                                      "skills": [100], "partners": ["ugent"], "coaches": [10]})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()
    assert len(json['projects']) == 3


def test_create_project_no_name(database_with_data: Session, auth_client: AuthClient):
    """Tests creating a project that has no name"""
    auth_client.admin()
    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()
    assert len(json['projects']) == 3
    response = \
        auth_client.post("/editions/ed2022/projects/",
                         # project has no name
                         json={
                             "number_of_students": 5,
                             "skills": [], "partners": [], "coaches": []})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()
    assert len(json['projects']) == 3


def test_patch_project(database_with_data: Session, auth_client: AuthClient):
    """Tests patching a project"""
    auth_client.admin()
    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()

    assert len(json['projects']) == 3

    response = auth_client.patch("/editions/ed2022/projects/1",
                                 json={"name": "patched",
                                       "number_of_students": 5,
                                       "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [1]})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = auth_client.get('/editions/ed2022/projects')
    json = response.json()

    assert len(json['projects']) == 3
    assert json['projects'][0]['name'] == 'patched'


def test_patch_project_non_existing_skills(database_with_data: Session, auth_client: AuthClient):
    """Tests patching a project with non-existing skills"""
    auth_client.admin()
    assert len(database_with_data.query(Skill).where(
        Skill.skill_id == 100).all()) == 0

    response = auth_client.patch("/editions/ed2022/projects/1",
                                 json={"name": "test1",
                                       "number_of_students": 1,
                                       "skills": [100], "partners": ["ugent"], "coaches": [1]})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = auth_client.get("/editions/ed2022/projects/1")
    json = response.json()
    assert 100 not in json["skills"]


def test_patch_project_non_existing_coach(database_with_data: Session, auth_client: AuthClient):
    """Tests patching a project with a coach that doesn't exist"""
    auth_client.admin()
    assert len(database_with_data.query(Student).where(
        Student.edition_id == 10).all()) == 0

    response = auth_client.patch("/editions/ed2022/projects/1",
                                 json={"name": "test2",
                                       "number_of_students": 1,
                                       "skills": [100], "partners": ["ugent"], "coaches": [10]})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = auth_client.get("/editions/ed2022/projects/1")
    json = response.json()
    assert 10 not in json["coaches"]


def test_patch_wrong_project(database_session: Session, auth_client: AuthClient):
    """Tests patching with wrong project info"""
    auth_client.admin()
    database_session.add(Edition(year=2022, name="ed2022"))
    project = Project(name="project", edition_id=1,
                      project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = \
        auth_client.patch("/editions/ed2022/projects/1",
        test_client.patch("/editions/ed2022/projects/1",
                          json={"name": "patched",
                                "skills": [], "partners": [], "coaches": []})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response2 = auth_client.get('/editions/ed2022/projects')
    json = response2.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == 'project'
