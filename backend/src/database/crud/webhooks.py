from sqlalchemy.orm import Session

from src.database.models import WebhookURL, Edition


def get_webhook(db: Session, uuid: str) -> WebhookURL:
    return db.query(WebhookURL).where(WebhookURL.uuid == uuid).one()


def create_webhook(db: Session, edition: Edition) -> WebhookURL:
    webhook_url: WebhookURL = WebhookURL(edition=edition)
    db.add(webhook_url)
    db.commit()
    print(webhook_url.uuid)
    return webhook_url
