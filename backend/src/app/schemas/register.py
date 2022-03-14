
from src.app.schemas.webhooks import CamelCaseModel

class NewUser(CamelCaseModel):
    name: str
    email: str
    pw: str
