from sqlalchemy.orm import Session

from src.app.schemas.register import NewUser
from src.database.models import Edition, InviteLink
from src.database.crud.register import create_user, create_auth_email, create_coach_request
from src.database.crud.invites import get_invite_link_by_uuid, delete_invite_link
from src.app.exceptions.register import FailedToAddNewUserException
from src.app.logic.security import get_password_hash


def create_request(db: Session, new_user: NewUser, edition: Edition) -> None:
    """Create a coach request. If something fails, the changes aren't committed"""
    transaction = db.begin_nested()
    invite_link: InviteLink = get_invite_link_by_uuid(db, new_user.uuid)
    try:
        user = create_user(db, new_user.name, new_user.email)
        create_auth_email(db, user, get_password_hash(new_user.pw))
        create_coach_request(db, user, edition)
        delete_invite_link(db, invite_link)
    except Exception as exception:
        transaction.rollback()
        raise FailedToAddNewUserException from exception
