from fastapi import APIRouter
from .schemas import WebhookEvent

router = APIRouter(prefix="/webhook")


@router.post("/{uuid}")
def webhook(data: WebhookEvent):
    return data
