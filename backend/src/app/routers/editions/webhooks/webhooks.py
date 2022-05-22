from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.logic.webhooks import process_webhook
from src.app.routers.tags import Tags
from src.app.schemas.webhooks import WebhookEvent, WebhookUrlResponse
from src.app.utils.dependencies import get_edition, require_admin, get_editable_edition
from src.database.crud.webhooks import get_webhook, create_webhook
from src.database.database import get_session
from src.database.models import Edition

webhooks_router = APIRouter(prefix="/webhooks", tags=[Tags.WEBHOOKS])


async def valid_uuid(uuid: str, database: AsyncSession = Depends(get_session)):
    """Verify if uuid is a valid uuid"""
    await get_webhook(database, uuid)


@webhooks_router.post("", response_model=WebhookUrlResponse, status_code=status.HTTP_201_CREATED,
                      dependencies=[Depends(require_admin)])
async def new(edition: Edition = Depends(get_editable_edition), database: AsyncSession = Depends(get_session)):
    """Create a new webhook for an edition"""
    return await create_webhook(database, edition)


@webhooks_router.post("/{uuid}", dependencies=[Depends(valid_uuid)], status_code=status.HTTP_201_CREATED)
async def webhook(data: WebhookEvent, edition: Edition = Depends(get_edition),
                  database: AsyncSession = Depends(get_session)):
    """Receive a webhook event, This is triggered by Tally"""
    try:
        await process_webhook(edition, data, database)
    except Exception as exception:
        # When processing fails, write the webhook data to a file to make sure it is not lost.
        with open(f'failed-webhook-{data.event_id}.json', 'w', encoding='utf-8') as file:
            file.write(data.json())
        raise exception  # Let the exception propagate further.
