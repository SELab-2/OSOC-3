from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.app.exceptions.parsing import MalformedUUIDError
from src.database.crud.util import paginate
from src.database.models import Edition, InviteLink


async def create_invite_link(db: AsyncSession, edition: Edition, email_address: str) -> InviteLink:
    """Create a new invite link"""
    link = InviteLink(target_email=email_address, edition=edition)
    db.add(link)
    await db.commit()
    return link


async def delete_invite_link(db: AsyncSession, invite_link: InviteLink, commit: bool = True):
    """Delete an invite link from the database"""
    await db.delete(invite_link)

    if commit:
        await db.commit()


def _get_pending_invites_for_edition_query(edition: Edition) -> Select:
    """Return the query for all InviteLinks linked to a given edition"""
    return select(InviteLink).where(InviteLink.edition == edition).order_by(InviteLink.invite_link_id)


async def get_pending_invites_for_edition(db: AsyncSession, edition: Edition) -> list[InviteLink]:
    """Returns a list with all InviteLinks linked to a given edition"""
    result = await db.execute(_get_pending_invites_for_edition_query(edition))
    return result.scalars().all()


async def get_pending_invites_for_edition_page(db: AsyncSession, edition: Edition, page: int) -> list[InviteLink]:
    """Returns a paginated list with all InviteLinks linked to a given edition"""
    result = await db.execute(paginate(_get_pending_invites_for_edition_query(edition), page))
    return result.scalars().all()


async def get_optional_invite_link_by_edition_and_email(db: AsyncSession, edition: Edition, email: str) -> InviteLink | None:
    """Return an optional invite link by edition and target_email"""
    query = select(InviteLink)\
        .where(InviteLink.edition == edition)\
        .where(InviteLink.target_email == email)
    result = await db.execute(query)
    return result.scalars().one_or_none()


async def get_invite_link_by_uuid(db: AsyncSession, invite_uuid: str | UUID) -> InviteLink:
    """Get an invite link by its id
    As the ids are auto-generated per row, there's no need to use the Edition
    from the path parameters as an extra filter
    """
    # Convert to UUID if necessary
    if isinstance(invite_uuid, str):
        try:
            invite_uuid = UUID(invite_uuid)
        except ValueError as value_error:
            # If conversion failed, then the input string was not a valid uuid
            raise MalformedUUIDError(str(invite_uuid)) from value_error

    query = select(InviteLink).where(InviteLink.uuid == invite_uuid)
    result = await db.execute(query)
    return result.scalars().one()
