from sqlalchemy.orm import Session
from starlette import status

from settings import DB_PAGE_SIZE
from src.database.models import Edition, Project, User, Partner
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

    response = auth_client.post("/editions/ed2022/projects", json={
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

    auth_client.post(f"/editions/{edition.name}/projects", json={
        "name": "test",
        "partners": ["ugent"],
        "coaches": [user.user_id]
    })
    auth_client.post(f"/editions/{edition.name}/projects", json={
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
    endpoint = f"/editions/{edition.name}/projects"

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
    response = auth_client.post(f"/editions/{edition.name}/projects", json={
        "partners": [],
        "coaches": []
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = auth_client.get(f"/editions/{edition.name}/projects/")
    assert len(response.json()['projects']) == 0


def test_patch_project(database_session: Session, auth_client: AuthClient):
    """Tests patching a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    partner: Partner = Partner(name="partner 1")
    user: User = User(name="user 1")
    project: Project = Project(name="project 1", edition=edition, partners=[partner], coaches=[user])
    database_session.add(project)
    database_session.commit()

    auth_client.admin()

    new_user: User = User(name="new user")
    database_session.add(new_user)
    database_session.commit()

    response = auth_client.patch(f"/editions/{edition.name}/projects/{project.project_id}", json={
        "name": "patched",
        "partners": ["ugent"],
        "coaches": [new_user.user_id]})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = auth_client.get(f'/editions/{edition.name}/projects')
    json = response.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == 'patched'
    assert len(json['projects'][0]['partners']) == 1
    assert json['projects'][0]['partners'][0]['name'] == 'ugent'
    assert len(json['projects'][0]['coaches']) == 1
    assert json['projects'][0]['coaches'][0]['name'] == new_user.name


def test_patch_project_non_existing_coach(database_session: Session, auth_client: AuthClient):
    """Tests patching a project with a coach that doesn't exist"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    database_session.add(project)
    database_session.commit()

    auth_client.admin()

    database_session.begin_nested()
    response = auth_client.patch(f"/editions/{edition.name}/projects/{project.project_id}", json={
        "name": "test2",
        "partners": [],
        "coaches": [10]
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
    assert len(response.json()['coaches']) == 0


def test_patch_wrong_project(database_session: Session, auth_client: AuthClient):
    """Tests patching with wrong project info"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    database_session.add(project)
    database_session.commit()

    auth_client.admin()

    database_session.begin_nested()
    response = auth_client.patch(f"/editions/{edition.name}/projects/{project.project_id}", json={
        "name": "patched",
        "partners": []
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = auth_client.get(f'/editions/{edition.name}/projects/')
    json = response.json()
    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == project.name


def test_create_project_old_edition(database_session: Session, auth_client: AuthClient):
    """test create a project for a readonly edition"""
    edition_22: Edition = Edition(year=2022, name="ed2022")
    edition_23: Edition = Edition(year=2023, name="ed2023")
    database_session.add(edition_22)
    database_session.add(edition_23)
    database_session.commit()

    auth_client.admin()

    response = auth_client.post(f"/editions/{edition_22.name}/projects", json={
        "name": "test",
        "partners": ["ugent"],
        "coaches": []
    })
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_search_project_name(database_session: Session, auth_client: AuthClient):
    """test search project on name"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(Project(name="project 1", edition=edition))
    database_session.add(Project(name="project 2", edition=edition))
    database_session.commit()

    auth_client.coach(edition)
    response = auth_client.get(f"/editions/{edition.name}/projects?name=1")
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["name"] == "project 1"


def test_search_project_coach(database_session: Session, auth_client: AuthClient):
    """test search project on coach"""
    edition: Edition = Edition(year=2022, name="ed2022")

    auth_client.coach(edition)

    database_session.add(Project(name="project 1", edition=edition))
    database_session.add(Project(name="project 2", edition=edition, coaches=[auth_client.user]))
    database_session.commit()

    response = auth_client.get(f"/editions/{edition.name}/projects/?coach=true")
    json = response.json()
    assert len(json["projects"]) == 1
    assert json["projects"][0]["name"] == "project 2"
    assert json["projects"][0]["coaches"][0]["userId"] == auth_client.user.user_id
