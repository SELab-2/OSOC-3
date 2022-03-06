from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.database.crud.webhooks import get_webhook, create_webhook
from src.app.routers.editions.webhooks.schemas import WebhookEvent, WebhookUrlResponse
from src.database.models import Edition
from src.app.utils.dependencies import get_edition
from src.app.routers.tags import Tags

webhooks_router = APIRouter(prefix="/webhook", tags=[Tags.WEBHOOKS])


def valid_uuid(uuid: str, db: Session = Depends(get_session)):
    get_webhook(db, uuid)


@webhooks_router.post("/", response_model=WebhookUrlResponse)  # TODO: check admin permission
def new(edition: Edition = Depends(get_edition), db: Session = Depends(get_session)):
    return create_webhook(db, edition)


@webhooks_router.post("/{uuid}", dependencies=[Depends(valid_uuid)])
def webhook(data: WebhookEvent, db: Session = Depends(get_session)):
    return data
