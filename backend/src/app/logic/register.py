import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exceptions.register import FailedToAddNewUserException
from src.app.logic.security import get_password_hash
from src.app.schemas.register import NewUser
from src.database.crud.invites import get_invite_link_by_uuid, delete_invite_link
from src.database.crud.register import create_coach_request, create_user, create_auth_email
from src.database.models import Edition, InviteLink


async def create_request(db: AsyncSession, new_user: NewUser, edition: Edition) -> None:
    """Create a coach request. If something fails, the changes aren't committed"""
    invite_link: InviteLink = await get_invite_link_by_uuid(db, new_user.uuid)

    try:
        # Make all functions in here not commit anymore,
        # so we can roll back at the end if we have to
        user = await create_user(db, new_user.name, commit=False)
        await create_auth_email(db, user, get_password_hash(new_user.pw), new_user.email, commit=False)
        await create_coach_request(db, user, edition, commit=False)
        await delete_invite_link(db, invite_link, commit=False)

        await db.commit()
    except sqlalchemy.exc.SQLAlchemyError as exception:
        await db.rollback()
        raise FailedToAddNewUserException from exception
