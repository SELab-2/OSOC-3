from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum

class NewDecision(CamelCaseModel):
    """the fields of a decision"""
    decision: DecisionEnum