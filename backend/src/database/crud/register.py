from sqlalchemy.orm import Session

from src.database.models import User

def create_user(db: Session, name: str, email: str) -> User:
    new_user: User = User(name="Jos", email="mail@email.com")
    db.add(new_user)
    db.commit()
    return new_user