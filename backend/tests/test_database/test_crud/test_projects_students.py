import pytest
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import Session

from src.app.schemas.projects import InputArgumentation
from src.database.crud.projects_students import (
    create_pr_suggestion,
    remove_project_role_suggestion,
    update_pr_suggestion,
    get_pr_suggestion_for_pr_by_student,
    get_optional_pr_suggestion_for_pr_by_student,
)
from src.database.models import Edition, Project, User, Skill, ProjectRole, Student, ProjectRoleSuggestion


def test_add_pr_suggestion(database_session: Session):
    """tests add student to a project"""
    db = database_session
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project1", edition=edition)
    user: User = User(name="coach1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True, edition=edition
    )
    skill: Skill = Skill(name="dab")
    db.add(user)
    db.add(project)
    db.add(edition)
    db.add(student)
    db.add(skill)
    db.commit()

    project_role: ProjectRole = ProjectRole(project=project, slots=1, skill=skill)
    db.add(project_role)
    db.commit()

    assert len(db.query(ProjectRoleSuggestion).where(ProjectRoleSuggestion.student == student).all()) == 0
    create_pr_suggestion(db, project_role, student, user, InputArgumentation())
    assert len(db.query(ProjectRoleSuggestion).where(ProjectRoleSuggestion.student == student).all()) == 1


def test_add_pr_suggestion_duplicate(database_session: Session):
    """tests add student to a project"""
    db = database_session
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project1", edition=edition)
    user: User = User(name="coach1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True, edition=edition
    )
    skill: Skill = Skill(name="dab")
    db.add(user)
    db.add(project)
    db.add(edition)
    db.add(student)
    db.add(skill)
    db.commit()

    project_role: ProjectRole = ProjectRole(project=project, slots=1, skill=skill)
    db.add(project_role)
    db.commit()

    create_pr_suggestion(db, project_role, student, user, InputArgumentation())
    with pytest.raises(IntegrityError):
        create_pr_suggestion(db, project_role, student, user, InputArgumentation())


def test_get_pr_suggestion(database_session: Session):
    """tests add student to a project"""
    db = database_session
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project1", edition=edition)
    user: User = User(name="coach1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True, edition=edition
    )
    skill: Skill = Skill(name="dab")
    db.add(user)
    db.add(project)
    db.add(edition)
    db.add(student)
    db.add(skill)
    db.commit()

    project_role: ProjectRole = ProjectRole(project=project, slots=1, skill=skill)
    db.add(project_role)
    db.commit()

    with pytest.raises(NoResultFound):
        get_pr_suggestion_for_pr_by_student(db, project_role, student)
    create_pr_suggestion(db, project_role, student, user, InputArgumentation())
    assert get_pr_suggestion_for_pr_by_student(db, project_role, student) is not None


def test_get_optional_pr_suggestion(database_session: Session):
    """tests add student to a project"""
    db = database_session
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project1", edition=edition)
    user: User = User(name="coach1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True, edition=edition
    )
    skill: Skill = Skill(name="dab")
    db.add(user)
    db.add(project)
    db.add(edition)
    db.add(student)
    db.add(skill)
    db.commit()

    project_role: ProjectRole = ProjectRole(project=project, slots=1, skill=skill)
    db.add(project_role)
    db.commit()

    assert get_optional_pr_suggestion_for_pr_by_student(db, project_role, student) is None
    create_pr_suggestion(db, project_role, student, user, InputArgumentation())
    assert get_optional_pr_suggestion_for_pr_by_student(db, project_role, student) is not None


def test_remove_student_from_project(database_session: Session):
    """test removing a student form a project"""
    db = database_session
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project1", edition=edition)
    user: User = User(name="coach1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True, edition=edition
    )
    skill: Skill = Skill(name="dab")
    db.add(user)
    db.add(project)
    db.add(edition)
    db.add(student)
    db.add(skill)
    db.commit()

    project_role: ProjectRole = ProjectRole(project=project, slots=1, skill=skill)
    db.add(project_role)
    db.commit()

    create_pr_suggestion(db, project_role, student, user, InputArgumentation())
    assert len(db.query(ProjectRoleSuggestion).where(ProjectRoleSuggestion.student == student).all()) == 1
    remove_project_role_suggestion(db, project_role, student)
    assert len(db.query(ProjectRoleSuggestion).where(ProjectRoleSuggestion.student == student).all()) == 0


def test_remove_student_from_project_not_assigned_to(database_session: Session):
    """test removing a student form a project that don't exist"""
    db = database_session
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project1", edition=edition)
    user: User = User(name="coach1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True, edition=edition
    )
    skill: Skill = Skill(name="dab")
    db.add(user)
    db.add(project)
    db.add(edition)
    db.add(student)
    db.add(skill)
    db.commit()

    project_role: ProjectRole = ProjectRole(project=project, slots=1, skill=skill)
    db.add(project_role)
    db.commit()

    with pytest.raises(NoResultFound):
        remove_project_role_suggestion(db, project_role, student)


def test_change_project_role(database_session: Session):
    """test change project role"""
    db = database_session
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project1", edition=edition)
    user: User = User(name="coach1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True, edition=edition
    )
    skill: Skill = Skill(name="dab")
    db.add(user)
    db.add(project)
    db.add(edition)
    db.add(student)
    db.add(skill)
    db.commit()

    project_role: ProjectRole = ProjectRole(project=project, slots=1, skill=skill)
    db.add(project_role)
    db.commit()

    create_pr_suggestion(db, project_role, student, user, InputArgumentation())
    assert len(db.query(ProjectRoleSuggestion).where(ProjectRoleSuggestion.student == student).all()) == 1

    updating_user: User = User(name="coach1")
    argumentation: InputArgumentation = InputArgumentation(argumentation="+")

    pr_suggestion: ProjectRoleSuggestion = get_pr_suggestion_for_pr_by_student(db, project_role, student)
    update_pr_suggestion(db, pr_suggestion, updating_user, argumentation)

    assert pr_suggestion.student == student
    assert pr_suggestion.drafter == updating_user
    assert pr_suggestion.argumentation == "+"
    assert pr_suggestion.project_role == project_role

    assert len(db.query(ProjectRoleSuggestion).where(ProjectRoleSuggestion.student == student).all()) == 1
