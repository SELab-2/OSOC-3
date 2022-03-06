from sqlalchemy.orm import Session

from src.database import models


def test_user_coach_request(database_session: Session):
    # Passing as user_id
    user = models.User(name="name", email="email1")
    database_session.add(user)
    database_session.commit()

    req = models.CoachRequest(user_id=user.user_id)
    database_session.add(req)
    database_session.commit()

    assert req.user == user

    # Check if passing as user instead of user_id works
    user = models.User(name="name", email="email2")
    database_session.add(user)
    database_session.commit()

    req = models.CoachRequest(user=user)
    database_session.add(req)
    database_session.commit()

    assert req.user_id == user.user_id


def test_project_partners(database_session: Session):
    project = models.Project(name="project")
    database_session.add(project)
    database_session.commit()

    partner = models.Partner(name="partner")
    database_session.add(project)
    database_session.commit()

    assert len(partner.projects) == 0
    assert len(project.partners) == 0

    partner.projects.append(project)
    database_session.commit()

    # Verify that appending to the list updates the association table
    # in both directions
    assert len(partner.projects) == 1
    assert partner.projects[0] == project

    assert len(project.partners) == 1
    assert project.partners[0] == partner
