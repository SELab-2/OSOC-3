from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Edition, Project, Skill, ProjectRole, Student, ProjectRoleSuggestion
from tests.utils.authorization import AuthClient


async def test_add_pr_suggestion(database_session: AsyncSession, auth_client: AuthClient):
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
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        resp = await auth_client.post(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}",
            json={"argumentation": "argumentation"}
        )
        assert resp.status_code == status.HTTP_201_CREATED
        json1 = resp.json()
        assert json1["projectRoleSuggestion"]["projectRoleSuggestionId"] == 1
        assert json1["projectRoleSuggestion"]["argumentation"] == 'argumentation'
        response2 = await auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
        json2 = response2.json()
        assert len(json2['projectRoles']) == 1
        assert len(json2['projectRoles'][0]['suggestions']) == 1
        assert json2['projectRoles'][0]['suggestions'][0]['argumentation'] == 'argumentation'


async def test_add_pr_suggestion_non_existing_student(database_session: AsyncSession, auth_client: AuthClient):
    """Tests adding a non-existing student to a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    database_session.add(project_role)
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        resp = await auth_client.post(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/0",
            json={"argumentation": "argumentation"}
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND
    
        response = await auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
        json = response.json()
        assert len(json['projectRoles']) == 1
        assert len(json['projectRoles'][0]['suggestions']) == 0


async def test_add_pr_suggestion_non_existing_pr(database_session: AsyncSession, auth_client: AuthClient):
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
    await database_session.commit()

    await auth_client.coach(edition)
    
    async with auth_client:
        resp = await auth_client.post(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/0/students/{student.student_id}",
            json={"argumentation": "argumentation"}
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert len((await database_session.execute(select(ProjectRoleSuggestion))).scalars().all()) == 0


async def test_add_pr_suggestion_readonly_edition(database_session: AsyncSession, auth_client: AuthClient):
    """tests add a student to a project from an old edition"""
    edition: Edition = Edition(year=2022, name="ed2022", readonly=True)
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
    await database_session.commit()

    await auth_client.coach(edition)

    await database_session.commit()

    async with auth_client:
        resp = await auth_client.post(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}",
            json={"argumentation": "argumentation"}
        )
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_change_pr_suggestion(database_session: AsyncSession, auth_client: AuthClient):
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
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        resp = await auth_client.patch(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}",
            json={"argumentation": "argumentation"}
        )
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        response2 = await auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
        json = response2.json()
        assert len(json['projectRoles']) == 1
        assert len(json['projectRoles'][0]['suggestions']) == 1
        assert json['projectRoles'][0]['suggestions'][0]['argumentation'] == 'argumentation'


async def test_change_pr_suggestion_non_existing_student(database_session: AsyncSession, auth_client: AuthClient):
    """Tests changing a non-existing student of a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    database_session.add(project_role)
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        resp = await auth_client.patch(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/0",
            json={"argumentation": "argumentation"}
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_change_pr_suggestion_non_existing_pr(database_session: AsyncSession, auth_client: AuthClient):
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
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        resp = await auth_client.patch(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/0/students/{student.student_id}",
            json={"argumentation": "argumentation"}
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_pr_suggestion(database_session: AsyncSession, auth_client: AuthClient):
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
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        resp = await auth_client.delete(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}"
        )
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        response2 = await auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
        print(response2.json())
        print((await database_session.execute(select(ProjectRole))).scalars().one().suggestions)
        json = response2.json()
        assert len(json['projectRoles']) == 1
        assert len(json['projectRoles'][0]['suggestions']) == 0


async def test_delete_pr_suggestion_multiple(database_session: AsyncSession, auth_client: AuthClient):
    """Tests deleting a student from a project, with a student being assigned to multiple project_roles"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    project2: Project = Project(name="project 2", edition=edition)
    skill: Skill = Skill(name="skill 1")
    project_role: ProjectRole = ProjectRole(project=project, skill=skill, slots=1)
    project_role2: ProjectRole = ProjectRole(project=project2, skill=skill, slots=1)
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
    pr_suggestion2: ProjectRoleSuggestion = ProjectRoleSuggestion(project_role=project_role2, student=student)
    database_session.add(pr_suggestion)
    database_session.add(pr_suggestion2)
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        resp = await auth_client.delete(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}"
        )
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        response2 = await auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
        json = response2.json()
        assert len(json['projectRoles']) == 1
        assert len(json['projectRoles'][0]['suggestions']) == 0


async def test_delete_pr_suggestion_non_existing_pr_suggestion(database_session: AsyncSession, auth_client: AuthClient):
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
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        resp = await auth_client.delete(
            f"/editions/{edition.name}/projects/{project.project_id}/roles/{project_role.project_role_id}/students/{student.student_id}"
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_get_conflicts(database_session: AsyncSession, auth_client: AuthClient):
    """Test getting the conflicts"""
    edition: Edition = Edition(year=2022, name="ed2022")
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

    database_session.add(Student(
        first_name="Jos2",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@gmail.com",
        phone_number="0487/86.24.46",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    ))

    database_session.add(ProjectRoleSuggestion(
        student=student,
        project_role=ProjectRole(
            skill=skill,
            slots=1,
            project=Project(
                name="project 1",
                edition=edition
            )
        )
    ))

    database_session.add(ProjectRoleSuggestion(
        student=student,
        project_role=ProjectRole(
            skill=skill,
            slots=1,
            project=Project(
                name="project 2",
                edition=edition
            )
        )
    ))
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(f"/editions/{edition.name}/projects/conflicts")
        json = response.json()
        assert len(json['conflictStudents']) == 1
        assert json['conflictStudents'][0]['studentId'] == student.student_id
        assert len(json['conflictStudents'][0]['prSuggestions']) == 2
