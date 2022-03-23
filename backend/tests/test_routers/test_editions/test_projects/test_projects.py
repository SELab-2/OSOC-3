
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from src.app.logic.projects_students import logic_add_student_project
from src.database.models import Edition, Project, Student, Skill, User


def test_get_projects(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = test_client.get("/editions/1/projects")
    json = response.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == "project"


def test_get_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = test_client.get("/editions/1/projects/1")
    json = response.json()

    assert json['name'] == 'project'


def test_delete_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = test_client.delete("/editions/1/projects/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_no_projects(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()

    response = test_client.delete("/editions/1/projects/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()

    response = \
        test_client.post("/editions/1/projects/",
                         json={"name": "test",
                               "number_of_students": 5,
                               "skills": [], "partners": [], "coaches": []})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['projectId'] == 1
    assert response.json()['name'] == 'test'

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == "test"


def test_create_wrong_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()

    response = \
        test_client.post("/editions/1/projects/",
                         # project has no name
                         json={
                               "number_of_students": 5,
                               "skills": [], "partners": [], "coaches": []})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects']) == 0


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
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == 'patched'


def test_patch_wrong_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    response = \
        test_client.patch("/editions/1/projects/1",
                          json={"name": "patched",
                                "skills": [], "partners": [], "coaches": []})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == 'project'


def test_add_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    resp = test_client.post("/editions/1/projects/1/students/1", json={"skill_id": 1, "drafter_id": 1})

    assert resp.status_code == status.HTTP_201_CREATED

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects'][0]['projectRoles']) == 1
    assert json['projects'][0]['projectRoles'][0]['skillId'] == 1


def test_add_wrong_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    resp = test_client.post("/editions/1/projects/1/students/1", json={"drafter_id": 1})

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects'][0]['projectRoles']) == 0


def test_change_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    logic_add_student_project(database_session, project, 1, 1, 1)
    resp1 = test_client.patch("/editions/1/projects/1/students/1", json={"skill_id": 2, "drafter_id": 2})

    assert resp1.status_code == status.HTTP_204_NO_CONTENT

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects'][0]['projectRoles']) == 1
    assert json['projects'][0]['projectRoles'][0]['skillId'] == 2


def test_change_wrong_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    logic_add_student_project(database_session, project, 1, 1, 1)
    resp1 = test_client.patch("/editions/1/projects/1/students/1", json={"skill_id": 2})

    assert resp1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects'][0]['projectRoles']) == 1
    assert json['projects'][0]['projectRoles'][0]['skillId'] == 1


def test_delete_student_project(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    logic_add_student_project(database_session, project, 1, 1, 1)
    resp = test_client.delete("/editions/1/projects/1/students/1")

    assert resp.status_code == status.HTTP_204_NO_CONTENT

    response2 = test_client.get('/editions/1/projects')
    json = response2.json()

    assert len(json['projects'][0]['projectRoles']) == 0


def test_delete_student_project_empty(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=2)
    database_session.add(project)
    database_session.commit()

    resp = test_client.delete("/editions/1/projects/1/students/1")

    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_get_conflicts(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    project = Project(name="project", edition_id=1, project_id=1, number_of_students=1)
    project2 = Project(name="project2", edition_id=1, project_id=3, number_of_students=1)
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
    response = test_client.get("/editions/1/projects/conflicts")
    json = response.json()
    assert len(json['conflictStudents']) == 1
    assert json['conflictStudents'][0]['student']['studentId'] == 1
    assert len(json['conflictStudents'][0]['projects']) == 2
