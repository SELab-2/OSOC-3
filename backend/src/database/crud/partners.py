from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Partner


async def create_partner(db: AsyncSession, name: str, commit: bool = True) -> Partner:
    """Create a partner given a name"""
    partner = Partner(name=name)
    db.add(partner)

    if commit:
        await db.flush()

    return partner


async def get_optional_partner_by_name(db: AsyncSession, name: str) -> Partner | None:
    """Returns an optional partner given a name"""
    return (await db.execute(select(Partner).where(Partner.name == name))).scalar_one_or_none()
