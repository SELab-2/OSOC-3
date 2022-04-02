from sqlalchemy.orm import Session

from src.app.utils.edition_readonly import check_readonly_edition
from src.database.models import WebhookURL, Edition


def get_webhook(database: Session, uuid: str) -> WebhookURL:
    """Retrieve a webhook by uuid"""
    return database.query(WebhookURL).where(WebhookURL.uuid == uuid).one()


def create_webhook(database: Session, edition: Edition) -> WebhookURL:
    """Create a webhook for a given edition"""
    check_readonly_edition(database, edition)

    webhook_url: WebhookURL = WebhookURL(edition=edition)
    database.add(webhook_url)
    database.commit()
    return webhook_url
