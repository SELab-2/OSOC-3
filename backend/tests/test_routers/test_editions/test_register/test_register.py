from json import dumps
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.database.models import Edition

def test_ok(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()
    response = test_client.post("/editions/1/register/email", data=dumps({"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"}))
    assert response.status_code == status.HTTP_201_CREATED
