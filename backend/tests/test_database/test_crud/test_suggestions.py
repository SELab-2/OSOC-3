import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from src.database.models import Suggestion, Student, User, Edition, Skill

from src.database.crud.suggestions import (create_suggestion, get_suggestions_of_student,
                                           get_suggestion_by_id, get_own_suggestion, delete_suggestion,
                                           update_suggestion,
                                           get_suggestions_of_student_by_type)
from src.database.enums import DecisionEnum


@pytest.fixture
async def database_with_data(database_session: AsyncSession):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Editions
    edition: Edition = Edition(year=2022, name="ed22")
    database_session.add(edition)
    await database_session.commit()

    # Users
    admin: User = User(name="admin", admin=True)
    coach1: User = User(name="coach1")
    coach2: User = User(name="coach2")
    database_session.add(admin)
    database_session.add(coach1)
    database_session.add(coach2)
    await database_session.commit()

    # Skill
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    skill4: Skill = Skill(name="skill4", description="something about skill4")
    skill5: Skill = Skill(name="skill5", description="something about skill5")
    skill6: Skill = Skill(name="skill6", description="something about skill6")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    database_session.add(skill4)
    database_session.add(skill5)
    database_session.add(skill6)
    await database_session.commit()

    # Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill6])
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    database_session.add(student01)
    database_session.add(student30)
    await database_session.commit()

    # Suggestion
    suggestion1: Suggestion = Suggestion(
        student=student01, coach=admin, argumentation="Good student", suggestion=DecisionEnum.YES)
    database_session.add(suggestion1)
    await database_session.commit()
    return database_session


async def test_create_suggestion_yes(database_with_data: AsyncSession):
    """Test creat a yes suggestion"""

    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    new_suggestion = await create_suggestion(
        database_with_data, user.user_id, student.student_id, DecisionEnum.YES, "This is a good student")

    suggestion: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id))).unique().scalars().one()

    assert new_suggestion == suggestion

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.YES
    assert suggestion.argumentation == "This is a good student"


async def test_create_suggestion_no(database_with_data: AsyncSession):
    """Test create a no suggestion"""

    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    new_suggestion = await create_suggestion(
        database_with_data, user.user_id, student.student_id, DecisionEnum.NO, "This is a not good student")

    suggestion: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id))).unique().scalars().one()

    assert new_suggestion == suggestion

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "This is a not good student"


async def test_create_suggestion_maybe(database_with_data: AsyncSession):
    """Test create a maybe suggestion"""

    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    new_suggestion = await create_suggestion(
        database_with_data, user.user_id, student.student_id, DecisionEnum.MAYBE, "Idk if it's good student")

    suggestion: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id))).unique().scalars().one()

    assert new_suggestion == suggestion

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.MAYBE
    assert suggestion.argumentation == "Idk if it's good student"


async def test_get_own_suggestion_existing(database_with_data: AsyncSession):
    """Test getting your own suggestion"""
    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().one()
    student1: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "josvermeulen@mail.com"))).unique().scalars().one()

    suggestion = await create_suggestion(database_with_data, user.user_id, student1.student_id, DecisionEnum.YES, "args")

    assert (await get_own_suggestion(database_with_data, student1.student_id, user.user_id)) == suggestion


async def test_get_own_suggestion_non_existing(database_with_data: AsyncSession):
    """Test getting your own suggestion when it doesn't exist"""
    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().one()
    student1: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "josvermeulen@mail.com"))).unique().scalars().one()

    assert (await get_own_suggestion(database_with_data, student1.student_id, user.user_id)) is None


async def test_get_own_suggestion_fields_none(database_with_data: AsyncSession):
    """Test getting your own suggestion when either of the fields are None
    This is really only to increase coverage, the case isn't possible in practice
    """
    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().one()
    student1: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "josvermeulen@mail.com"))).unique().scalars().one()
    await create_suggestion(database_with_data, user.user_id, student1.student_id, DecisionEnum.YES, "args")

    assert (await get_own_suggestion(database_with_data, None, user.user_id)) is None
    assert (await get_own_suggestion(database_with_data, student1.student_id, None)) is None


async def test_one_coach_two_students(database_with_data: AsyncSession):
    """Test that one coach can write multiple suggestions"""

    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().one()
    student1: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().one()
    student2: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "josvermeulen@mail.com"))).unique().scalars().one()

    await create_suggestion(database_with_data, user.user_id,
                      student1.student_id, DecisionEnum.YES, "This is a good student")
    await create_suggestion(database_with_data, user.user_id, student2.student_id,
                      DecisionEnum.NO, "This is a not good student")

    suggestion1: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student1.student_id))).unique().scalars().one()
    assert suggestion1.coach == user
    assert suggestion1.student == student1
    assert suggestion1.suggestion == DecisionEnum.YES
    assert suggestion1.argumentation == "This is a good student"

    suggestion2: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student2.student_id))).unique().scalars().one()
    assert suggestion2.coach == user
    assert suggestion2.student == student2
    assert suggestion2.suggestion == DecisionEnum.NO
    assert suggestion2.argumentation == "This is a not good student"


async def test_multiple_suggestions_about_same_student(database_with_data: AsyncSession):
    """Test get multiple suggestions about the same student"""

    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    await create_suggestion(database_with_data, user.user_id, student.student_id,
                      DecisionEnum.MAYBE, "Idk if it's good student")
    with pytest.raises(IntegrityError):
        await create_suggestion(database_with_data, user.user_id,
                          student.student_id, DecisionEnum.YES, "This is a good student")


async def test_get_suggestions_of_student(database_with_data: AsyncSession):
    """Test get all suggestions of a student"""

    user1: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    user2: User = (await database_with_data.execute(select(
        User).where(User.name == "coach2"))).scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    await create_suggestion(database_with_data, user1.user_id, student.student_id,
                      DecisionEnum.MAYBE, "Idk if it's good student")
    await create_suggestion(database_with_data, user2.user_id,
                      student.student_id, DecisionEnum.YES, "This is a good student")
    suggestions_student = await get_suggestions_of_student(
        database_with_data, student.student_id)

    assert len(suggestions_student) == 2
    assert suggestions_student[0].student == student
    assert suggestions_student[1].student == student


async def test_get_suggestion_by_id(database_with_data: AsyncSession):
    """Test get suggestion by id"""
    suggestion: Suggestion = await get_suggestion_by_id(database_with_data, 1)
    assert suggestion.student_id == 1
    assert suggestion.coach_id == 1
    assert suggestion.suggestion == DecisionEnum.YES
    assert suggestion.argumentation == "Good student"


async def test_get_suggestion_by_id_non_existing(database_with_data: AsyncSession):
    """Test you get an error when you search an id that don't exist"""
    with pytest.raises(NoResultFound):
        await get_suggestion_by_id(database_with_data, 900)


async def test_delete_suggestion(database_with_data: AsyncSession):
    """Test delete suggestion"""

    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    await create_suggestion(database_with_data, user.user_id,
                      student.student_id, DecisionEnum.YES, "This is a good student")
    suggestion: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id))).unique().scalars().one()

    await delete_suggestion(database_with_data, suggestion)

    suggestions: list[Suggestion] = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id))).unique().scalars().all()
    assert len(suggestions) == 0


async def test_update_suggestion(database_with_data: AsyncSession):
    """Test update suggestion"""

    user: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    await create_suggestion(database_with_data, user.user_id,
                      student.student_id, DecisionEnum.YES, "This is a good student")
    suggestion: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id))).unique().scalars().one()

    await update_suggestion(database_with_data, suggestion,
                      DecisionEnum.NO, "Not that good student")

    new_suggestion: Suggestion = (await database_with_data.execute(select(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id))).unique().scalars().one()
    assert new_suggestion.suggestion == DecisionEnum.NO
    assert new_suggestion.argumentation == "Not that good student"


async def test_get_suggestions_of_student_by_type(database_with_data: AsyncSession):
    """Tests get suggestion of a student by type of suggestion"""
    user1: User = (await database_with_data.execute(select(
        User).where(User.name == "coach1"))).unique().scalars().first()
    user2: User = (await database_with_data.execute(select(
        User).where(User.name == "coach2"))).scalars().first()
    user3: User = (await database_with_data.execute(select(
        User).where(User.name == "admin"))).scalars().first()
    student: Student = (await database_with_data.execute(select(Student).where(
        Student.email_address == "marta.marquez@example.com"))).unique().scalars().first()

    await create_suggestion(database_with_data, user1.user_id, student.student_id,
                      DecisionEnum.MAYBE, "Idk if it's good student")
    await create_suggestion(database_with_data, user2.user_id,
                      student.student_id, DecisionEnum.YES, "This is a good student")
    await create_suggestion(database_with_data, user3.user_id,
                      student.student_id, DecisionEnum.NO, "This is not a good student")
    suggestions_student_yes = await get_suggestions_of_student_by_type(
        database_with_data, student.student_id, DecisionEnum.YES)
    suggestions_student_no = await get_suggestions_of_student_by_type(
        database_with_data, student.student_id, DecisionEnum.NO)
    suggestions_student_maybe = await get_suggestions_of_student_by_type(
        database_with_data, student.student_id, DecisionEnum.MAYBE)
    assert len(suggestions_student_yes) == 1
    assert len(suggestions_student_no) == 1
    assert len(suggestions_student_maybe) == 1
