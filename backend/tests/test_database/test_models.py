from sqlalchemy.orm import Session

from src.database import models


def test_user_coach_request(db):
    # Passing as user_id
    user = models.User(name="name", email="email1")
    db.add(user)
    db.commit()

    req = models.CoachRequest(user_id=user.user_id)
    db.add(req)
    db.commit()

    assert req.user == user

    # Check if passing as user instead of user_id works
    user = models.User(name="name", email="email2")
    db.add(user)
    db.commit()

    req = models.CoachRequest(user=user)
    db.add(req)
    db.commit()

    assert req.user_id == user.user_id


def test_project_partners(db):
    project = models.Project(name="project")
    db.add(project)
    db.commit()

    partner = models.Partner(name="partner")
    db.add(project)
    db.commit()

    assert len(partner.projects) == 0
    assert len(project.partners) == 0

    partner.projects.append(project)
    db.commit()

    # Verify that appending to the list updates the association table
    # in both directions
    assert len(partner.projects) == 1
    assert partner.projects[0] == project

    assert len(project.partners) == 1
    assert project.partners[0] == partner
