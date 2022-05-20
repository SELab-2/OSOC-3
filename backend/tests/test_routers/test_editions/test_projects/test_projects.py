import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings import DB_PAGE_SIZE
from src.database.models import Edition, Project, Skill, User, Partner
from tests.utils.authorization import AuthClient


async def test_get_projects_paginated(database_session: AsyncSession, auth_client: AuthClient):
    """test get all projects paginated"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(Project(name=f"Project {i}", edition=edition))
    await database_session.commit()

    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects?page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['projects']) == DB_PAGE_SIZE
        response = await auth_client.get("/editions/ed2022/projects?page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['projects']) == round(
            DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


async def test_get_project(database_session: AsyncSession, auth_client: AuthClient):
    """Tests get a specific project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(edition=edition, name="project 1")
    database_session.add(project)
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(f"/editions/{edition.name}/projects/{project.project_id}")
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json['projectId'] == project.project_id
        assert json['name'] == project.name
        assert len(json['coaches']) == 0
        assert len(json['partners']) == 0
        assert len(json['projectRoles']) == 0


async def test_delete_project(database_session: AsyncSession, auth_client: AuthClient):
    """Tests delete a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(edition=edition, name="project 1")
    database_session.add(project)
    await database_session.commit()

    await auth_client.admin()
    endpoint = f"/editions/{edition.name}/projects/{project.project_id}"

    async with auth_client:
        response = await auth_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK
        response = await auth_client.delete(endpoint)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await auth_client.get(endpoint)
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_project_not_found(database_session: AsyncSession, auth_client: AuthClient):
    """Tests delete a project that doesn't exist"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    await auth_client.admin()
    async with auth_client:
        response = await auth_client.delete(f"/editions/{edition.name}/projects/400")
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_project(database_session: AsyncSession, auth_client: AuthClient):
    """Tests creating a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    database_session.add(edition)
    database_session.add(user)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
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


async def test_create_project_same_partner(database_session: AsyncSession, auth_client: AuthClient):
    """Tests that creating a project doesn't create a partner if the partner already exists"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    database_session.add(edition)
    database_session.add(user)
    await database_session.commit()

    assert len((await database_session.execute(select(Partner))).unique().scalars().all()) == 0

    await auth_client.admin()
    async with auth_client:

        await auth_client.post(f"/editions/{edition.name}/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })
        await auth_client.post(f"/editions/{edition.name}/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })
        assert len((await database_session.execute(select(Partner))).unique().scalars().all()) == 1


@pytest.mark.skip(reason="The async database rolls back everything, even with nested query")
async def test_create_project_non_existing_coach(database_session: AsyncSession, auth_client: AuthClient):
    """Tests creating a project with a coach that doesn't exist"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    await auth_client.admin()
    endpoint = f"/editions/{edition.name}/projects"

    await database_session.begin_nested()
    async with auth_client:
        response = await auth_client.post(endpoint, json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [0]
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get(f"/editions/{edition.name}/projects/")
        assert len(response.json()['projects']) == 0


async def test_create_project_no_name(database_session: AsyncSession, auth_client: AuthClient):
    """Tests creating a project that has no name"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    await auth_client.admin()

    await database_session.begin_nested()
    async with auth_client:
        response = await auth_client.post(f"/editions/{edition.name}/projects", json={
            "partners": [],
            "coaches": []
        })

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = await auth_client.get(f"/editions/{edition.name}/projects/", follow_redirects=True)
        assert len(response.json()['projects']) == 0


async def test_patch_project(database_session: AsyncSession, auth_client: AuthClient):
    """Tests patching a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    partner: Partner = Partner(name="partner 1")
    user: User = User(name="user 1")
    project: Project = Project(name="project 1", edition=edition, partners=[
                               partner], coaches=[user])
    database_session.add(project)
    await database_session.commit()

    await auth_client.admin()

    new_user: User = User(name="new user")
    database_session.add(new_user)
    await database_session.commit()

    async with auth_client:
        response = await auth_client.patch(f"/editions/{edition.name}/projects/{project.project_id}", json={
            "name": "patched",
            "partners": ["ugent"],
            "coaches": [new_user.user_id]})
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = await auth_client.get(f'/editions/{edition.name}/projects')
        json = response.json()

    assert len(json['projects']) == 1
    assert json['projects'][0]['name'] == 'patched'
    assert len(json['projects'][0]['partners']) == 1
    assert json['projects'][0]['partners'][0]['name'] == 'ugent'
    assert len(json['projects'][0]['coaches']) == 1
    assert json['projects'][0]['coaches'][0]['name'] == new_user.name


@pytest.mark.skip(reason="The async database rolls back everything, even with nested query")
async def test_patch_project_non_existing_coach(database_session: AsyncSession, auth_client: AuthClient):
    """Tests patching a project with a coach that doesn't exist"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    database_session.add(project)
    await database_session.commit()

    await auth_client.admin()

    await database_session.begin_nested()
    async with auth_client:
        response = await auth_client.patch(f"/editions/{edition.name}/projects/{project.project_id}", json={
            "name": "test2",
            "partners": [],
            "coaches": [10]
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND

    response = await auth_client.get(f'/editions/{edition.name}/projects/{project.project_id}')
    assert len(response.json()['coaches']) == 0


async def test_patch_wrong_project(database_session: AsyncSession, auth_client: AuthClient):
    """Tests patching with wrong project info"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    database_session.add(project)
    await database_session.commit()

    await auth_client.admin()

    await database_session.begin_nested()
    async with auth_client:
        response = await auth_client.patch(f"/editions/{edition.name}/projects/{project.project_id}", json={
            "name": "patched",
            "partners": []
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = await auth_client.get(f'/editions/{edition.name}/projects/', follow_redirects=True)
        json = response.json()
        assert len(json['projects']) == 1
        assert json['projects'][0]['name'] == project.name


async def test_create_project_old_edition(database_session: AsyncSession, auth_client: AuthClient):
    """test create a project for a readonly edition"""
    edition_22: Edition = Edition(year=2022, name="ed2022")
    edition_23: Edition = Edition(year=2023, name="ed2023")
    database_session.add(edition_22)
    database_session.add(edition_23)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post(f"/editions/{edition_22.name}/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": []
        })
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_search_project_name(database_session: AsyncSession, auth_client: AuthClient):
    """test search project on name"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(Project(name="project 1", edition=edition))
    database_session.add(Project(name="project 2", edition=edition))
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(f"/editions/{edition.name}/projects?name=1")
        assert len(response.json()["projects"]) == 1
        assert response.json()["projects"][0]["name"] == "project 1"


async def test_search_project_coach(database_session: AsyncSession, auth_client: AuthClient):
    """test search project on coach"""
    edition: Edition = Edition(year=2022, name="ed2022")

    await auth_client.coach(edition)

    database_session.add(Project(name="project 1", edition=edition))
    database_session.add(
        Project(name="project 2", edition=edition, coaches=[auth_client.user]))
    await database_session.commit()

    async with auth_client:
        response = await auth_client.get(f"/editions/{edition.name}/projects?coach=true", follow_redirects=True)
        json = response.json()
        assert len(json["projects"]) == 1
        assert json["projects"][0]["name"] == "project 2"
        assert json["projects"][0]["coaches"][0]["userId"] == auth_client.user.user_id


async def test_delete_project_role(database_session: AsyncSession, auth_client: AuthClient):
    """test delete a project role"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": 1
        })
        response = await auth_client.get("/editions/ed2022/projects/1/roles")
        assert len(response.json()["projectRoles"]) == 1
        response = await auth_client.delete("/editions/ed2022/projects/1/roles/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await auth_client.get("/editions/ed2022/projects/1/roles")
        assert len(response.json()["projectRoles"]) == 0


async def test_make_project_role(database_session: AsyncSession, auth_client: AuthClient):
    """test make a project role"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": 1
        })
        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert json["projectRoleId"] == 1
        assert json["projectId"] == 1
        assert json["description"] == "description"
        assert json["skill"]["skillId"] == 1
        assert json["slots"] == 1


async def test_make_project_role_negative_slots(database_session: AsyncSession, auth_client: AuthClient):
    """test make a project role"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": -1
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_make_project_role_zero_slots(database_session: AsyncSession, auth_client: AuthClient):
    """test make a project role"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": 0
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_update_project_role(database_session: AsyncSession, auth_client: AuthClient):
    """test update a project role"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": 1
        })
        assert response.status_code == status.HTTP_201_CREATED
        response = await auth_client.patch("/editions/ed2022/projects/1/roles/1", json={
            "skill_id": 1,
            "description": "changed",
            "slots": 2
        })
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await auth_client.get("/editions/ed2022/projects/1/roles")
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["projectRoles"]) == 1
        assert json["projectRoles"][0]["projectRoleId"] == 1
        assert json["projectRoles"][0]["projectId"] == 1
        assert json["projectRoles"][0]["description"] == "changed"
        assert json["projectRoles"][0]["skill"]["skillId"] == 1
        assert json["projectRoles"][0]["slots"] == 2


async def test_update_project_role_negative_slots(database_session: AsyncSession, auth_client: AuthClient):
    """test update a project role with negative slots"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": 1
        })
        assert response.status_code == status.HTTP_201_CREATED
        response = await auth_client.patch("/editions/ed2022/projects/1/roles/1", json={
            "skill_id": 1,
            "description": "description",
            "slots": -1
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_update_project_role_zero_slots(database_session: AsyncSession, auth_client: AuthClient):
    """test update a project role with zero slots"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": 1
        })
        assert response.status_code == status.HTTP_201_CREATED
        response = await auth_client.patch("/editions/ed2022/projects/1/roles/1", json={
            "skill_id": 1,
            "description": "description",
            "slots": 0
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_project_role(database_session: AsyncSession, auth_client: AuthClient):
    """test get project role"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach 1")
    skill: Skill = Skill(name="Skill1")
    database_session.add(edition)
    database_session.add(user)
    database_session.add(skill)
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/ed2022/projects", json={
            "name": "test",
            "partners": ["ugent"],
            "coaches": [user.user_id]
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["projectId"] == 1
        response = await auth_client.post("/editions/ed2022/projects/1/roles", json={
            "skill_id": 1,
            "description": "description",
            "slots": 1
        })
        assert response.status_code == status.HTTP_201_CREATED
        response = await auth_client.get("/editions/ed2022/projects/1/roles")
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["projectRoles"]) == 1
        assert json["projectRoles"][0]["projectRoleId"] == 1
        assert json["projectRoles"][0]["projectId"] == 1
        assert json["projectRoles"][0]["description"] == "description"
        assert json["projectRoles"][0]["skill"]["skillId"] == 1
        assert json["projectRoles"][0]["slots"] == 1
