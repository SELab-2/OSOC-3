from sqlalchemy.ext.asyncio import AsyncSession

import src.database.crud.partners as crud

from src.database.models import Partner


async def get_or_create_partners_by_name(db: AsyncSession, names: list[str], commit: bool = True) -> list[Partner]:
    """Return a list of partners, when a partner with the name does not exist, create it"""
    partners: list[Partner] = []
    for partner_name in names:
        partner = await crud.get_optional_partner_by_name(db, partner_name)
        if partner is None:
            partners.append(await crud.create_partner(db, partner_name, commit=commit))
        else:
            partners.append(partner)
    return partners
