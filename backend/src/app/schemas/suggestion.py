from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum

class NewSuggestion(CamelCaseModel):
    """The fields of a suggestion"""
    student_id: int
    coach_id: int
    suggestion: DecisionEnum
    argumentation: str