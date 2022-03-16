from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.database.crud.webhooks import get_webhook, create_webhook
from src.app.schemas.webhooks import WebhookEvent, WebhookUrlResponse
from src.database.models import Edition
from src.app.utils.dependencies import get_edition
from src.app.routers.tags import Tags
from src.app.logic.webhooks import process_webhook
from starlette import status

webhooks_router = APIRouter(prefix="/webhooks", tags=[Tags.WEBHOOKS])


def valid_uuid(uuid: str, database: Session = Depends(get_session)):
    """Verify if uuid is a valid uuid"""
    get_webhook(database, uuid)


# TODO: check admin permission
@webhooks_router.post("/", response_model=WebhookUrlResponse, status_code=status.HTTP_201_CREATED)
def new(edition: Edition = Depends(get_edition), database: Session = Depends(get_session)):
    """Create e new webhook for an edition"""
    return create_webhook(database, edition)


@webhooks_router.post("/{uuid}", dependencies=[Depends(valid_uuid)], status_code=status.HTTP_201_CREATED)
def webhook(data: WebhookEvent, edition: Edition = Depends(get_edition), database: Session = Depends(get_session)):
    """Receive a webhook event, This is triggered by Tally"""
    try:
        process_webhook(edition, data, database)
    except Exception as exception:
        # When processing fails, write the webhook data to a file to make sure it is not lost.
        with open(f'failed-webhook-{data.event_id}.json', 'w', encoding='utf-8') as file:
            file.write(data.json())
        raise exception  # Let the exception propagate further.
