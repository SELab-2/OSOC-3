import sqlalchemy.exc
from sqlalchemy.orm import Session

from src.app.schemas.register import NewUser
from src.app.utils.edition_readonly import check_readonly_edition
from src.database.models import Edition, InviteLink
from src.database.crud.register import create_coach_request, create_user, create_auth_email
from src.database.crud.invites import get_invite_link_by_uuid, delete_invite_link
from src.app.exceptions.register import FailedToAddNewUserException
from src.app.logic.security import get_password_hash


def create_request(db: Session, new_user: NewUser, edition: Edition) -> None:
    """Create a coach request. If something fails, the changes aren't committed"""
    check_readonly_edition(db, edition)

    invite_link: InviteLink = get_invite_link_by_uuid(db, new_user.uuid)

    with db.begin_nested() as transaction:
        try:
            # Make all functions in here not commit anymore,
            # so we can roll back at the end if we have to
            user = create_user(db, new_user.name, commit=False)
            create_auth_email(db, user, get_password_hash(new_user.pw), new_user.email, commit=False)
            create_coach_request(db, user, edition, commit=False)
            delete_invite_link(db, invite_link, commit=False)

            transaction.commit()
        except sqlalchemy.exc.SQLAlchemyError as exception:
            transaction.rollback()
            raise FailedToAddNewUserException from exception
