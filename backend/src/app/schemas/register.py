from src.app.schemas.invites import EmailAddress

class NewUser(EmailAddress):
    name: str
    pw: str

