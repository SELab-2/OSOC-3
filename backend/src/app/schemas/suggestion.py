from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum
from src.app.schemas.users import User, user_model_to_schema
from src.database.models import Suggestion as Suggestion_model


class NewSuggestion(CamelCaseModel):
    """The fields of a suggestion"""
    suggestion: DecisionEnum
    argumentation: str


class Suggestion(CamelCaseModel):
    """
    Model to represent a Suggestion
    Sent as a response to API /GET requests
    """

    suggestion_id: int
    coach: User
    suggestion: DecisionEnum
    argumentation: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class SuggestionListResponse(CamelCaseModel):
    """
    A list of suggestions models
    """
    suggestions: list[Suggestion]


class SuggestionResponse(CamelCaseModel):
    """
    the suggestion that is created
    """
    suggestion: Suggestion


def suggestion_model_to_schema(suggestion_model: Suggestion_model) -> Suggestion:
    """Create Suggestion Schema from Suggestion Model"""
    coach: User = user_model_to_schema(suggestion_model.coach)
    return Suggestion(suggestion_id=suggestion_model.suggestion_id,
                      coach=coach,
                      suggestion=suggestion_model.suggestion,
                      argumentation=suggestion_model.argumentation)
