from dataclasses import dataclass
from fastapi import APIRouter


# Router for the base/home routes
base_router = APIRouter()


@dataclass
class DummyResponse:
    message: str


@base_router.get("/", response_model=DummyResponse)
async def base_get():
    """Placeholder dummy route"""
    return DummyResponse(message="Hello, world!")
