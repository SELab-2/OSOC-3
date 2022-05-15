from uuid import UUID

from src.app.schemas.invites import EmailAddress
from src.app.schemas.utils import CamelCaseModel


class EmailRegister(EmailAddress):
    """Scheme used for a new user created with email-password authentication"""
    name: str
    pw: str
    uuid: UUID


class GitHubRegister(CamelCaseModel):
    """Scheme used for a new user created with GitHub OAuth"""
    code: str
    uuid: UUID
