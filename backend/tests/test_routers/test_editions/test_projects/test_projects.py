from sqlalchemy.orm import Session
from starlette import status

from settings import DB_PAGE_SIZE
from src.database.models import Edition, Project, User, Skill, Student, Partner
from tests.utils.authorization import AuthClient


def test_get_projects_paginated(database_session: Session, auth_client: AuthClient):
    """test get all projects paginated"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(Project(name=f"Project {i}", edition=edition))
    database_session.commit()

    auth_client.admin()

    response = auth_client.get("/editions/ed2022/projects?page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['projects']) == DB_PAGE_SIZE
    response = auth_client.get("/editions/ed2022/projects?page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['projects']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


def test_get_project(database_session: Session, auth_client: AuthClient):
    """Tests get a specific project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(edition=edition, name="project 1")
    database_session.add(project)
    database_session.commit()

    auth_client.coach(edition)
    response = auth_client.get(f"/editions/{edition.name}/projects/{project.project_id}")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['projectId'] == project.project_id
    assert json['name'] == project.name
    assert len(json['coaches']) == 0
    assert len(json['partners']) == 0
    assert len(json['projectRoles']) == 0


def test_delete_project(database_session: Session, auth_client: AuthClient):
    """Tests delete a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(edition=edition, name="project 1")
    database_session.add(project)
    database_session.commit()

    auth_client.admin()
    endpoint = f"/editions/{edition.name}/projects/{project.project_id}"

    response = auth_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK
    response = auth_client.delete(endpoint)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = auth_client.get(endpoint)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_project_not_found(database_session: Session, auth_client: AuthClient):
    """Tests delete a project that doesn't exist"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    auth_client.admin()
    response = auth_client.delete(f"/editions/{edition.name}/projects/400")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_project(database_session: Session, auth_client: AuthClient):
    """Tests creating a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    database_session.add(edition)
    database_session.add(user)
    database_session.commit()

    auth_client.admin()

    response = auth_client.post("/editions/ed2022/projects/", json={
        "name": "test",
        "partners": ["ugent"],
        "coaches": [user.user_id]
    })

    assert response.status_code == status.HTTP_201_CREATED
    json: dict = response.json()
    assert "projectId" in json
    assert json["name"] == "test"
    assert json["partners"][0]["name"] == "ugent"
    assert json["coaches"][0]["name"] == user.name
    assert len(json["projectRoles"]) == 0


def test_create_project_same_partner(database_session: Session, auth_client: AuthClient):
    """Tests that creating a project doesn't create a partner if the partner already exists"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    database_session.add(edition)
    database_session.add(user)
    database_session.commit()

    assert len(database_session.query(Partner).all()) == 0

    auth_client.admin()

    auth_client.post(f"/editions/{edition.name}/projects/", json={
        "name": "test",
        "partners": ["ugent"],
        "coaches": [user.user_id]
    })
    auth_client.post(f"/editions/{edition.name}/projects/", json={
        "name": "test",
        "partners": ["ugent"],
        "coaches": [user.user_id]
    })
    assert len(database_session.query(Partner).all()) == 1


def test_create_project_non_existing_coach(database_session: Session, auth_client: AuthClient):
    """Tests creating a project with a coach that doesn't exist"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    auth_client.admin()
    endpoint = f"/editions/{edition.name}/projects/"
    print(database_session.query(Edition).all())

    database_session.begin_nested()
    response = auth_client.post(endpoint, json={
        "name": "test",
        "partners": ["ugent"],
        "coaches": [0]
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = auth_client.get(f"/editions/{edition.name}/projects/")
    assert len(response.json()['projects']) == 0


def test_create_project_no_name(database_session: Session, auth_client: AuthClient):
    """Tests creating a project that has no name"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    auth_client.admin()

    database_session.begin_nested()
    response = auth_client.post("/editions/ed2022/projects/", json={
        "partners": [],
        "coaches": []
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = auth_client.get('/editions/ed2022/projects')
    assert len(response.json()['projects']) == 0


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
                          json={"name": "patched",
                                "skills": [], "partners": [], "coaches": []})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response2 = auth_client.get('/editions/ed2022/projects')
    json = response2.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == 'project'


def test_create_project_old_edition(database_with_data: Session, auth_client: AuthClient):
    """test create a project for a readonly edition"""
    auth_client.admin()
    database_with_data.add(Edition(year=2023, name="ed2023"))
    database_with_data.commit()

    response = \
        auth_client.post("/editions/ed2022/projects/",
                         json={"name": "test",
                               "number_of_students": 5,
                               "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [1]})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_search_project_name(database_with_data: Session, auth_client: AuthClient):
    """test search project on name"""
    auth_client.admin()
    response = auth_client.get("/editions/ed2022/projects/?name=super")
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["name"] == "super nice project"


def test_search_project_coach(database_with_data: Session, auth_client: AuthClient):
    """test search project on coach"""
    auth_client.admin()
    user: User = database_with_data.query(User).where(User.name == "Pytest Admin").one()
    auth_client.post("/editions/ed2022/projects/",
                     json={"name": "test",
                           "number_of_students": 2,
                           "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [user.user_id]})
    response = auth_client.get("/editions/ed2022/projects/?coach=true")
    print(response.json())
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["name"] == "test"
    assert response.json()["projects"][0]["coaches"][0]["userId"] == user.user_id
