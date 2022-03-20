from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import DecisionEnum

class NewSuggestion(CamelCaseModel):
    """The fields of a suggestion"""
    suggestion: DecisionEnum
    argumentation: str

class User(CamelCaseModel): #TODO: delete this when user is on develop and use that one
    """
    Model to represent a Coach
    Sent as a response to API /GET requests
    """
    user_id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class Suggestion(CamelCaseModel):
    """
    Model to represent a Suggestion
    Sent as a response to API /GET requests
    """

    suggestion_id: int
    coach : User
    suggestion: DecisionEnum
    argumentation: str

    class Config:
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