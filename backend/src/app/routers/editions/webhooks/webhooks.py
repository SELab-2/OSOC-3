from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.database.crud.webhooks import get_webhook, create_webhook
from src.app.schemas.webhooks import WebhookEvent, WebhookUrlResponse
from src.database.models import Edition
from src.app.utils.dependencies import get_edition
from src.app.routers.tags import Tags
from src.app.logic.webhooks import process_webhook

webhooks_router = APIRouter(prefix="/webhooks", tags=[Tags.WEBHOOKS])


def valid_uuid(uuid: str, db: Session = Depends(get_session)):
    get_webhook(db, uuid)


@webhooks_router.post("/", response_model=WebhookUrlResponse)  # TODO: check admin permission
def new(edition: Edition = Depends(get_edition), db: Session = Depends(get_session)):
    return create_webhook(db, edition)


@webhooks_router.post("/{uuid}", dependencies=[Depends(valid_uuid)])
def webhook(data: WebhookEvent, edition: Edition = Depends(get_edition), db: Session = Depends(get_session)):
    try:
        process_webhook(edition, data, db)
    except Exception as e:  # When processing fails, write the webhook data to a file to make sure it is not lost.
        with open(f'failed-webhook-{data.event_id}.json') as f:
            f.write(data.json())
        raise e  # Let the exception propagate further.
    return "OK"
