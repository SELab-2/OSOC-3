from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Edition, Project, User, Skill, ProjectRole, Student, ProjectRoleSuggestion
from tests.utils.authorization import AuthClient


def test_add_pr_suggestion(database_session: Session, auth_client: AuthClient):
    """tests add a student to a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )
    database_session.add(project_role)
    database_session.add(student)
    database_session.commit()

    auth_client.coach(edition)

    resp = auth_client.post(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}",
        json={"argumentation": "argumentation"}
    )

    assert resp.status_code == status.HTTP_201_CREATED

    response2 = auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
    json = response2.json()
    assert len(json['projectRoles']) == 1
    assert len(json['projectRoles'][0]['suggestions']) == 1
    assert json['projectRoles'][0]['suggestions'][0]['argumentation'] == 'argumentation'


def test_add_pr_suggestion_non_existing_student(database_session: Session, auth_client: AuthClient):
    """Tests adding a non-existing student to a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    database_session.add(project_role)
    database_session.commit()

    auth_client.coach(edition)

    resp = auth_client.post(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/0",
        json={"argumentation": "argumentation"}
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    response = auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
    json = response.json()
    assert len(json['projectRoles']) == 1
    assert len(json['projectRoles'][0]['suggestions']) == 0


def test_add_pr_suggestion_non_existing_pr(database_session: Session, auth_client: AuthClient):
    """Tests adding a non-existing student to a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )
    database_session.add(project)
    database_session.add(student)
    database_session.add(skill)
    database_session.commit()

    auth_client.coach(edition)

    resp = auth_client.post(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/0/students/{student.student_id}",
        json={"argumentation": "argumentation"}
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert len(database_session.query(ProjectRoleSuggestion).all()) == 0


def test_add_pr_suggestion_old_edition(database_session: Session, auth_client: AuthClient):
    """tests add a student to a project from an old edition"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )
    database_session.add(project_role)
    database_session.add(student)
    database_session.add(Edition(year=2023, name="ed2023"))
    database_session.commit()

    auth_client.coach(edition)

    database_session.commit()

    resp = auth_client.post(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}",
        json={"argumentation": "argumentation"}
    )
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_change_pr_suggestion(database_session: Session, auth_client: AuthClient):
    """Tests changing a student's project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )
    pr_suggestion: ProjectRoleSuggestion = ProjectRoleSuggestion(project_role=project_role, student=student)
    database_session.add(pr_suggestion)
    database_session.commit()

    auth_client.coach(edition)

    resp = auth_client.patch(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}",
        json={"argumentation": "argumentation"}
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    response2 = auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
    json = response2.json()
    assert len(json['projectRoles']) == 1
    assert len(json['projectRoles'][0]['suggestions']) == 1
    assert json['projectRoles'][0]['suggestions'][0]['argumentation'] == 'argumentation'


def test_change_pr_suggestion_non_existing_student(database_session: Session, auth_client: AuthClient):
    """Tests changing a non-existing student of a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    database_session.add(project_role)
    database_session.commit()

    auth_client.coach(edition)

    resp = auth_client.patch(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/0",
        json={"argumentation": "argumentation"}
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_change_pr_suggestion_non_existing_pr(database_session: Session, auth_client: AuthClient):
    """Tests deleting a student from a project that isn't assigned"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )
    database_session.add(project)
    database_session.add(student)
    database_session.add(skill)
    database_session.commit()

    auth_client.coach(edition)

    resp = auth_client.patch(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/0/students/{student.student_id}",
        json={"argumentation": "argumentation"}
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_delete_pr_suggestion(database_session: Session, auth_client: AuthClient):
    """Tests deleting a student from a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )
    pr_suggestion: ProjectRoleSuggestion = ProjectRoleSuggestion(project_role=project_role, student=student)
    database_session.add(pr_suggestion)
    database_session.commit()

    auth_client.coach(edition)
    resp = auth_client.delete(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}"
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    response2 = auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
    json = response2.json()
    assert len(json['projectRoles']) == 1
    assert len(json['projectRoles'][0]['suggestions']) == 0


def test_delete_pr_suggestion_non_existing_pr_suggestion(database_session: Session, auth_client: AuthClient):
    """Tests deleting a pr_suggestion that doesn't exist"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )
    database_session.add(project_role)
    database_session.add(student)
    database_session.commit()

    auth_client.coach(edition)

    resp = auth_client.delete(
        f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}"
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_get_conflicts(database_session: Session, current_edition: Edition, auth_client: AuthClient):
    """Test getting the conflicts"""
    auth_client.coach(current_edition)
    response = auth_client.get("/editions/ed2022/projects/conflicts")
    json = response.json()
    assert len(json['conflictStudents']) == 1
    assert json['conflictStudents'][0]['student']['studentId'] == 1
    assert len(json['conflictStudents'][0]['projects']) == 2


def test_add_student_project_already_confirmed(database_session: Session, current_edition: Edition,
                                               auth_client: AuthClient):
    """A project_role can't be created if the student involved has already been confirmed elsewhere"""
    auth_client.coach(current_edition)

    resp = auth_client.post("/editions/ed2022/projects/1/students/4", json={"skill_id": 3})

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_confirm_project_role(database_session: Session, auth_client: AuthClient):
    """Confirm a project role for a student without conflicts"""
    auth_client.admin()
    resp = auth_client.post(
        "/editions/ed2022/projects/1/students/3", json={"skill_id": 3})

    assert resp.status_code == status.HTTP_201_CREATED

    response2 = auth_client.post(
        "/editions/ed2022/projects/1/students/3/confirm")

    assert response2.status_code == status.HTTP_204_NO_CONTENT
    pr = database_session.query(ProjectRole).where(ProjectRole.student_id == 3) \
        .where(ProjectRole.project_id == 1).one()
    assert pr.definitive is True


def test_confirm_project_role_conflict(database_session: Session, auth_client: AuthClient):
    """A student who is part of a conflict can't have their project_role confirmed"""
    auth_client.admin()
    response2 = auth_client.post(
        "/editions/ed2022/projects/1/students/1/confirm")

    assert response2.status_code == status.HTTP_409_CONFLICT
