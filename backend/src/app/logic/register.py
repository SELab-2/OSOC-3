from click import edit
from sqlalchemy.orm import Session

from src.app.schemas.register import NewUser
from src.database.models import Edition

def create_user(db: Session, edition: Edition, new_user: NewUser):
    return