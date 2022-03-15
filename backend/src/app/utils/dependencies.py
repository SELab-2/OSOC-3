from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.crud.editions import get_edition_by_id
from src.database.crud.invites import get_invite_link_by_uuid
from src.database.database import get_session
from src.database.models import Edition, InviteLink


# TODO: Might be nice to use a more descriptive year number here than primary id.
def get_edition(edition_id: int, database: Session = Depends(get_session)) -> Edition:
    """Get an edition from the database, given the id in the path"""
    return get_edition_by_id(database, edition_id)


def get_invite_link(invite_uuid: str, db: Session = Depends(get_session)) -> InviteLink:
    """Get an invite link from the database, given the id in the path"""
    return get_invite_link_by_uuid(db, invite_uuid)
