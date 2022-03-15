from sqlalchemy.orm import Session

from src.database.models import WebhookURL, Edition


def get_webhook(database: Session, uuid: str) -> WebhookURL:
    """Retrieve a webhook by uuid"""
    return database.query(WebhookURL).where(WebhookURL.uuid == uuid).one()


def create_webhook(database: Session, edition: Edition) -> WebhookURL:
    """Create a webhook for a given edition"""
    webhook_url: WebhookURL = WebhookURL(edition=edition)
    database.add(webhook_url)
    database.commit()
    print(webhook_url.uuid)
    return webhook_url
