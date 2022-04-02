from sqlalchemy.orm import Session

from src.app.exceptions.editions import ReadOnlyEditionException
from src.database.crud.editions import latest_edition
from src.database.models import Edition


def check_readonly_edition(db: Session, edition: Edition):
    latest = latest_edition(db)
    if edition != latest:
        raise ReadOnlyEditionException
