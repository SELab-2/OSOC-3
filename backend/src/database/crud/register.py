from sqlalchemy.orm import Session

from src.database.models import User

def create_user(db: Session, name: str, email: str) -> User:
    user = User(name="Jos", email="mail@email.com")
    db.add(user)
    db.commit()
    return user