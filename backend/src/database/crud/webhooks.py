from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import WebhookURL, Edition


async def get_webhook(database: AsyncSession, uuid: str) -> WebhookURL:
    """Retrieve a webhook by uuid"""
    return (await database.execute(select(WebhookURL).where(WebhookURL.uuid == uuid))).scalar_one()


async def create_webhook(database: AsyncSession, edition: Edition) -> WebhookURL:
    """Create a webhook for a given edition"""
    webhook_url: WebhookURL = WebhookURL(edition=edition)
    database.add(webhook_url)
    await database.commit()
    return webhook_url
