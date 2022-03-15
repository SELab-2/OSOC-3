from json import dumps

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app.logic.projects_students import logic_add_student_project
from src.database.models import Edition, Project, Student, Skill, User


def test_get_projects(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = test_client.get("/editions/1/projects")
    json = response.json()
    print(json)


def test_get_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = test_client.get("/editions/1/projects/1")
    json = response.json()
    print(json)


def test_delete_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = test_client.delete("/editions/1/projects/1")
    print(response)


def test_create_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    # project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    # database_session.add(project)
    database_session.commit()

    response = \
        test_client.post("/editions/1/projects/",
                         json={"name": "test",
                               "number_of_students": 5,
                               "skills": [], "partners": [], "coaches": []})
    print(response)
    response2 = test_client.get('/editions/1/projects')
    json = response2.json()
    print(json)


def test_patch_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = \
        test_client.patch("/editions/1/projects/1",
                          json={"name": "patched",
                                "number_of_students": 5,
                                "skills": [], "partners": [], "coaches": []})
    print(response)
    response2 = test_client.get('/editions/1/projects')
    json = response2.json()
    print(json)


def test_add_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    student = Student(student_id=1, first_name="test", last_name="person", preferred_name="test",
                      email_address="a@b.com",
                      alumni=False, edition_id=1)
    skill = Skill(skill_id=1, name="test_skill")
    skill = Skill(skill_id=2, name="test_skill2")
    user = User(user_id=1, name="testuser", email="b@c.com")

    database_session.add(project)
    database_session.commit()

    print("test_add")
    resp = test_client.post("/editions/1/projects/1/students/1", json={"skill_id": 1, "drafter_id": 1})
    print(resp)
    response2 = test_client.get('/editions/1/projects')
    json = response2.json()
    print(json)


def test_change_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    student = Student(student_id=1, first_name="test", last_name="person", preferred_name="test",
                      email_address="a@b.com",
                      alumni=False, edition_id=1)
    skill = Skill(skill_id=1, name="test_skill")
    skill = Skill(skill_id=2, name="test_skill2")
    user = User(user_id=1, name="testuser", email="b@c.com")

    database_session.add(project)
    database_session.commit()

    print("test_change:")
    logic_add_student_project(database_session, project, 1, 1, 1)
    resp1 = test_client.patch("/editions/1/projects/1/students/1", json={"skill_id": 2, "drafter_id": 2})
    print(resp1)
    response2 = test_client.get('/editions/1/projects')
    json = response2.json()
    print(json)


def test_delete_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    student = Student(student_id=1, first_name="test", last_name="person", preferred_name="test",
                      email_address="a@b.com",
                      alumni=False, edition_id=1)
    skill = Skill(skill_id=1, name="test_skill")
    user = User(user_id=1, name="testuser", email="b@c.com")

    database_session.add(project)
    database_session.commit()

    logic_add_student_project(database_session, project, 1, 1, 1)
    test_client.delete("/editions/1/projects/1/students/1")
    response2 = test_client.get('/editions/1/projects')
    json = response2.json()
    print(json)


def test_get_conflicts(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=1)
    project2 = Project(name="project2", edition_id=1, project_id=2, number_of_students=1)
    student = Student(student_id=1, first_name="test", last_name="person", preferred_name="test",
                      email_address="a@b.com",
                      alumni=False, edition_id=1)
    skill = Skill(skill_id=1, name="test_skill")
    skill2 = Skill(skill_id=2, name="test_skill2")
    user = User(user_id=1, name="testuser", email="b@c.com")
    database_session.add(project)
    database_session.add(project2)
    database_session.add(student)
    database_session.add(skill)
    database_session.add(skill2)
    database_session.add(user)
    database_session.commit()

    logic_add_student_project(database_session, project, 1, 1, 1)
    logic_add_student_project(database_session, project2, 1, 2, 1)
    response2 = test_client.get("/editions/1/projects/conflicts")
    json = response2.json()
    print(json)
