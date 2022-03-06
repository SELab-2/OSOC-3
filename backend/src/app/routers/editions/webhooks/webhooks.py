from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.database.crud.webhooks import get_webhook, create_webhook
from .schemas import WebhookEvent, WebhookUrlResponse
from src.database.models import Edition
from src.app.utils.dependencies import get_edition

router = APIRouter(prefix="/webhook", tags=['Webhooks'])


def valid_uuid(uuid: str, db: Session = Depends(get_session)):
    get_webhook(db, uuid)


@router.post("/", response_model=WebhookUrlResponse)  # TODO: check admin permission
def new(edition: Edition = Depends(get_edition), db: Session = Depends(get_session)):
    return create_webhook(db, edition)


@router.post("/{uuid}", dependencies=[Depends(valid_uuid)])
def webhook(data: WebhookEvent, db: Session = Depends(get_session)):
    return data
