from uuid import UUID
from src.app.schemas.invites import EmailAddress


class NewUser(EmailAddress):
    """The scheme of a new user"""
    name: str
    pw: str
    uuid: UUID
