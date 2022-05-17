import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.skills import SkillBase
from src.database.crud import skills as crud
from src.database.models import Skill


async def test_get_skill_by_id_exists(database_session: AsyncSession):
    """Test getting a skill when it exists"""
    skill = Skill(name="skill")
    database_session.add(skill)
    await database_session.commit()

    found = await crud.get_skill_by_id(database_session, skill.skill_id)
    assert found == skill


async def test_get_skill_by_id_doesnt_exist(database_session: AsyncSession):
    """Test getting a skill when it doesn't exist"""
    with pytest.raises(NoResultFound):
        await crud.get_skill_by_id(database_session, 1)


async def test_create_skill(database_session: AsyncSession):
    """Test creating a skill"""
    await crud.create_skill(database_session, SkillBase(name="name"))

    skills = (await database_session.execute(select(Skill).where(Skill.name == "name"))).scalars().all()
    assert len(skills) == 1


async def test_delete_skill_present(database_session: AsyncSession):
    """Test deleting a skill when it exists"""
    skill = await crud.create_skill(database_session, SkillBase(name="name"))
    await crud.delete_skill(database_session, skill.skill_id)

    skills = (await database_session.execute(select(Skill).where(Skill.name == "name"))).scalars().all()
    assert len(skills) == 0


async def test_delete_skill_not_present(database_session: AsyncSession):
    """Test deleting a skill when it doesn't exist"""
    with pytest.raises(NoResultFound):
        await crud.delete_skill(database_session, 1)


async def test_create_skill_if_not_present_not_present(database_session: AsyncSession):
    """Test conditionally creating a skill when it doesn't exist"""
    assert await crud.create_skill_if_not_present(database_session, "name")
    skills = (await database_session.execute(select(Skill).where(Skill.name == "name"))).scalars().all()
    assert len(skills) == 1


async def test_create_skill_if_not_present_present(database_session: AsyncSession):
    """Test conditionally creating a skill when it does exist"""
    assert await crud.create_skill_if_not_present(database_session, "name")
    assert not await crud.create_skill_if_not_present(database_session, "name")
    skills = (await database_session.execute(select(Skill).where(Skill.name == "name"))).scalars().all()
    assert len(skills) == 1
