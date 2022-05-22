from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.crud.partners import create_partner, get_optional_partner_by_name
from src.database.models import Partner

async def test_create_partner_flush(database_session: AsyncSession):
    """test create partner flush"""
    partners: list[Partner] = (await database_session.execute(select(Partner))).scalars().all()
    assert len(partners) == 0
    await create_partner(database_session, "Ugent", True)
    partners: list[Partner] = (await database_session.execute(select(Partner))).scalars().all()
    assert len(partners) == 1
    assert partners[0].name == "Ugent"


async def test_optional_partner_by_name(database_session: AsyncSession):
    """test get partner by name or get none"""
    partner: Partner = await get_optional_partner_by_name(database_session, "Ugent")
    assert partner is None
    await create_partner(database_session, "Ugent", True)
    partner: Partner = await get_optional_partner_by_name(database_session, "Ugent")
    assert partner.name == "Ugent"
