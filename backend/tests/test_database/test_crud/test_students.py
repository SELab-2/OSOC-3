import datetime
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from src.database.models import Student, User, Edition, Skill, DecisionEmail
from src.database.enums import DecisionEnum, EmailStatusEnum
from src.database.crud.students import (create_email, get_last_emails_of_students, get_student_by_id,
                                        set_definitive_decision_on_student,
                                        delete_student, get_students, get_emails)
from src.app.schemas.students import CommonQueryParams, EmailsSearchQueryParams


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
    skill1: Skill = Skill(name="skill1")
    skill2: Skill = Skill(name="skill2")
    skill3: Skill = Skill(name="skill3")
    skill4: Skill = Skill(name="skill4")
    skill5: Skill = Skill(name="skill5")
    skill6: Skill = Skill(name="skill6")
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
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    database_session.add(student01)
    database_session.add(student30)
    await database_session.commit()

    # DecisionEmail
    decision_email: DecisionEmail = DecisionEmail(
        student=student01, decision=EmailStatusEnum.APPROVED, date=datetime.datetime.now())
    database_session.add(decision_email)
    await database_session.commit()

    return database_session


async def test_get_student_by_id(database_with_data: AsyncSession):
    """Tests if you get the right student"""
    student: Student = await get_student_by_id(database_with_data, 1)
    assert student.first_name == "Jos"
    assert student.last_name == "Vermeulen"
    assert student.student_id == 1
    assert student.email_address == "josvermeulen@mail.com"


async def test_no_student(database_with_data: AsyncSession):
    """Tests if you get an error for a not existing student"""
    with pytest.raises(NoResultFound):
        await get_student_by_id(database_with_data, 5)


async def test_definitive_decision_on_student_yes(database_with_data: AsyncSession):
    """Tests for definitive decision yes"""
    student: Student = await get_student_by_id(database_with_data, 1)
    await set_definitive_decision_on_student(
        database_with_data, student, DecisionEnum.YES)
    assert student.decision == DecisionEnum.YES


async def test_definitive_decision_on_student_maybe(database_with_data: AsyncSession):
    """Tests for definitive decision maybe"""
    student: Student = await get_student_by_id(database_with_data, 1)
    await set_definitive_decision_on_student(
        database_with_data, student, DecisionEnum.MAYBE)
    assert student.decision == DecisionEnum.MAYBE


async def test_definitive_decision_on_student_no(database_with_data: AsyncSession):
    """Tests for definitive decision no"""
    student: Student = await get_student_by_id(database_with_data, 1)
    await set_definitive_decision_on_student(
        database_with_data, student, DecisionEnum.NO)
    assert student.decision == DecisionEnum.NO


async def test_delete_student(database_with_data: AsyncSession):
    """Tests for deleting a student"""
    student: Student = await get_student_by_id(database_with_data, 1)
    await delete_student(database_with_data, student)
    with pytest.raises(NoResultFound):
        await get_student_by_id(database_with_data, 1)


async def test_get_all_students(database_with_data: AsyncSession):
    """test get all students"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    students = await get_students(database_with_data, edition, CommonQueryParams())
    assert len(students) == 2


async def test_search_students_on_first_name(database_with_data: AsyncSession):
    """test"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    students = await get_students(database_with_data, edition, CommonQueryParams(name="Jos"))
    assert len(students) == 1


async def test_search_students_on_last_name(database_with_data: AsyncSession):
    """tests search on last name"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    students = await get_students(database_with_data, edition, CommonQueryParams(name="Vermeulen"))
    assert len(students) == 1


async def test_search_students_on_between_first_and_last_name(database_with_data: AsyncSession):
    """tests search on between first- and last name"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    students = await get_students(database_with_data, edition, CommonQueryParams(name="os V"))
    assert len(students) == 1


async def test_search_students_alumni(database_with_data: AsyncSession):
    """tests search on alumni"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    students = await get_students(database_with_data, edition, CommonQueryParams(alumni=True))
    assert len(students) == 1


async def test_search_students_student_coach(database_with_data: AsyncSession):
    """tests search on student coach"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    students = await get_students(database_with_data, edition, CommonQueryParams(student_coach=True))
    assert len(students) == 1


async def test_search_students_one_skill(database_with_data: AsyncSession):
    """tests search on one skill"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    skill: Skill = (await database_with_data.execute(select(Skill).where(Skill.name == "skill1"))).scalar_one()
    students = await get_students(database_with_data, edition, CommonQueryParams(), skills=[skill])
    assert len(students) == 1


async def test_search_students_multiple_skills(database_with_data: AsyncSession):
    """tests search on multiple skills"""
    edition: Edition = (await database_with_data.execute(select(Edition).where(Edition.edition_id == 1))).scalar_one()
    skills: list[Skill] = [
        (await database_with_data.execute(select(Skill).where(Skill.name == "skill4"))).scalar_one(),
        (await database_with_data.execute(select(Skill).where(Skill.name == "skill5"))).scalar_one(),
    ]
    students = await get_students(database_with_data, edition, CommonQueryParams(), skills=skills)
    assert len(students) == 1


async def test_get_emails(database_with_data: AsyncSession):
    """tests to get emails"""
    student: Student = await get_student_by_id(database_with_data, 1)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 1
    student = await get_student_by_id(database_with_data, 2)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 0


async def test_create_email_applied(database_with_data: AsyncSession):
    """test create email applied"""
    student: Student = await get_student_by_id(database_with_data, 2)
    await create_email(database_with_data, student, EmailStatusEnum.APPLIED)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 1
    assert emails[0].decision == EmailStatusEnum.APPLIED


async def test_create_email_awaiting_project(database_with_data: AsyncSession):
    """test create email awaiting project"""
    student: Student = await get_student_by_id(database_with_data, 2)
    await create_email(database_with_data, student, EmailStatusEnum.AWAITING_PROJECT)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 1
    assert emails[0].decision == EmailStatusEnum.AWAITING_PROJECT


async def test_create_email_approved(database_with_data: AsyncSession):
    """test create email approved"""
    student: Student = await get_student_by_id(database_with_data, 2)
    await create_email(database_with_data, student, EmailStatusEnum.APPROVED)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 1
    assert emails[0].decision == EmailStatusEnum.APPROVED


async def test_create_email_contract_confirmed(database_with_data: AsyncSession):
    """test create email contract confirmed"""
    student: Student = await get_student_by_id(database_with_data, 2)
    await create_email(database_with_data, student,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 1
    assert emails[0].decision == EmailStatusEnum.CONTRACT_CONFIRMED


async def test_create_email_contract_declined(database_with_data: AsyncSession):
    """test create email contract declined"""
    student: Student = await get_student_by_id(database_with_data, 2)
    await create_email(database_with_data, student,
                       EmailStatusEnum.CONTRACT_DECLINED)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 1
    assert emails[0].decision == EmailStatusEnum.CONTRACT_DECLINED


async def test_create_email_rejected(database_with_data: AsyncSession):
    """test create email rejected"""
    student: Student = await get_student_by_id(database_with_data, 2)
    await create_email(database_with_data, student, EmailStatusEnum.REJECTED)
    emails: list[DecisionEmail] = await get_emails(database_with_data, student)
    assert len(emails) == 1
    assert emails[0].decision == EmailStatusEnum.REJECTED


async def test_get_last_emails_of_students(database_with_data: AsyncSession):
    """tests get last email of all students that got an email"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.REJECTED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    edition2: Edition = Edition(year=2023, name="ed2023")
    database_with_data.add(edition)
    student: Student = Student(first_name="Mehmet", last_name="Dizdar", preferred_name="Mehmet",
                               email_address="mehmet.dizdar@example.com", phone_number="(787)-938-6216", alumni=True,
                               wants_to_be_student_coach=False, edition=edition2, skills=[])
    database_with_data.add(student)
    await database_with_data.commit()
    await create_email(database_with_data, student,
                       EmailStatusEnum.REJECTED)

    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[]))
    assert len(emails) == 2
    assert emails[0].student_id == 1
    assert emails[0].decision == EmailStatusEnum.CONTRACT_CONFIRMED
    assert emails[1].student_id == 2
    assert emails[1].decision == EmailStatusEnum.REJECTED


async def test_get_last_emails_of_students_filter_applied(database_with_data: AsyncSession):
    """tests get all emails where last emails is applied"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student2,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[EmailStatusEnum.APPLIED]))

    assert len(emails) == 1
    assert emails[0].student_id == 2
    assert emails[0].decision == EmailStatusEnum.APPLIED


async def test_get_last_emails_of_students_filter_awaiting_project(database_with_data: AsyncSession):
    """tests get all emails where last emails is awaiting project"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.AWAITING_PROJECT)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[EmailStatusEnum.AWAITING_PROJECT]))

    assert len(emails) == 1
    assert emails[0].student_id == 2
    assert emails[0].decision == EmailStatusEnum.AWAITING_PROJECT


async def test_get_last_emails_of_students_filter_approved(database_with_data: AsyncSession):
    """tests get all emails where last emails is approved"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.APPROVED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[EmailStatusEnum.APPROVED]))

    assert len(emails) == 1
    assert emails[0].student_id == 2
    assert emails[0].decision == EmailStatusEnum.APPROVED


async def test_get_last_emails_of_students_filter_contract_confirmed(database_with_data: AsyncSession):
    """tests get all emails where last emails is contract confirmed"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[EmailStatusEnum.CONTRACT_CONFIRMED]))

    assert len(emails) == 1
    assert emails[0].student_id == 2
    assert emails[0].decision == EmailStatusEnum.CONTRACT_CONFIRMED


async def test_get_last_emails_of_students_filter_contract_declined(database_with_data: AsyncSession):
    """tests get all emails where last emails is contract declined"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.CONTRACT_DECLINED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[EmailStatusEnum.CONTRACT_DECLINED]))

    assert len(emails) == 1
    assert emails[0].student_id == 2
    assert emails[0].decision == EmailStatusEnum.CONTRACT_DECLINED


async def test_get_last_emails_of_students_filter_rejected(database_with_data: AsyncSession):
    """tests get all emails where last emails is rejected"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.REJECTED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[EmailStatusEnum.REJECTED]))

    assert len(emails) == 1
    assert emails[0].student_id == 2
    assert emails[0].decision == EmailStatusEnum.REJECTED


async def test_get_last_emails_of_students_first_name(database_with_data: AsyncSession):
    """tests get all emails where last emails is first name"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.REJECTED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(name="Jos", email_status=[]))

    assert len(emails) == 1
    assert emails[0].student_id == 1
    assert emails[0].decision == EmailStatusEnum.CONTRACT_CONFIRMED


async def test_get_last_emails_of_students_last_name(database_with_data: AsyncSession):
    """tests get all emails where last emails is last name"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.REJECTED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(name="Vermeulen", email_status=[]))

    assert len(emails) == 1
    assert emails[0].student_id == 1
    assert emails[0].decision == EmailStatusEnum.CONTRACT_CONFIRMED


async def test_get_last_emails_of_students_between_first_and_last_name(database_with_data: AsyncSession):
    """tests get all emails where last emails is between first- and last name"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student1,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student2,
                       EmailStatusEnum.REJECTED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(name="os V", email_status=[]))

    assert len(emails) == 1
    assert emails[0].student_id == 1
    assert emails[0].decision == EmailStatusEnum.CONTRACT_CONFIRMED


async def test_get_last_emails_of_students_filter_mutliple_status(database_with_data: AsyncSession):
    """tests get all emails where last emails is applied"""
    student1: Student = await get_student_by_id(database_with_data, 1)
    student2: Student = await get_student_by_id(database_with_data, 2)
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await create_email(database_with_data, student2,
                       EmailStatusEnum.APPLIED)
    await create_email(database_with_data, student1,
                       EmailStatusEnum.CONTRACT_CONFIRMED)
    emails: list[DecisionEmail] = await get_last_emails_of_students(
        database_with_data, edition, EmailsSearchQueryParams(email_status=[
            EmailStatusEnum.APPLIED,
            EmailStatusEnum.CONTRACT_CONFIRMED
        ]))

    assert len(emails) == 2
    assert emails[0].student_id == 1
    assert emails[0].decision == EmailStatusEnum.CONTRACT_CONFIRMED
    assert emails[1].student_id == 2
    assert emails[1].decision == EmailStatusEnum.APPLIED
