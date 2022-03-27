from uuid import UUID
from src.app.schemas.invites import EmailAddress


class NewUser(EmailAddress):
    """
    The scheme of a new user
    The email address will be stored in AuthEmail, but is included here to easily create a user
    """
    name: str
    pw: str
    uuid: UUID
