from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
from tests.fill_database import fill_database
from src.database.models import Suggestion, Student, User


#def test_test(database_session: Session, test_client: TestClient):
#    fill_database(database_session)
#    email = "coach1@noutlook.be"
#    password = "wachtwoord"
#    form = {
#        "username": email,
#        "password": password
#    }
#    d = test_client.post("/login/token", data=form).json()
#    print(d)
#    r = test_client.post("/editions/1/students/1/suggestions/", headers={"Authorization": str(d)})
#    #r = test_client.post("/editions/1/students/1/suggestions/")
#    print(r.json())
#    assert False


"""
def test_ok(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()
    response = test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.
"""