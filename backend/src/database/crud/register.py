from curses.ascii import US
from click import edit
from sqlalchemy.orm import Session

from src.database.models import Edition, User

def create_user(db: Session, edition: Edition, name: str, email: str) -> User:
    user = User(name=name, email=email, admin=False, editions=[edition])
    db.add(user)
    db.commit()
    return user