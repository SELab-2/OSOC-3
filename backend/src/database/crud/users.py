from src.database.models import User, UserRole
from sqlalchemy.orm import Session


def get_users_from_edition(db: Session, edition_id: int) -> list[User]:
    """Get all users from the given edition"""

    coaches = db.query(User).join(UserRole).where(UserRole.edition_id == edition_id).all()

    # TODO: admins (depends on changes in db)

    return coaches
