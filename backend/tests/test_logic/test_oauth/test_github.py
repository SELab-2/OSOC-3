from unittest.mock import AsyncMock

from pydantic import ValidationError
import pytest

from src.app.exceptions.register import InvalidGitHubCode
from src.app.logic.oauth import github as logic
from src.app.logic.oauth.github import get_github_profile


async def test_get_github_access_token_valid():
    """Test getting the access token when the response succeeds"""
    http_session = AsyncMock()
    response = AsyncMock()
    http_session.post.return_value = response
    response.json.return_value = {"access_token": "at", "scope": "read:user,user:email"}

    # If this doesn't throw an error then everything is okay
    await logic.get_github_access_token(http_session, "code")


async def test_get_github_access_token_error():
    """Test getting the access token when the response fails"""
    http_session = AsyncMock()
    response = AsyncMock()
    http_session.post.return_value = response
    response.json.return_value = {"error": "exists", "error_description": "description"}

    with pytest.raises(InvalidGitHubCode):
        await logic.get_github_access_token(http_session, "code")


async def test_get_github_access_token_missing_scopes():
    """Test getting the access token when the user removes some of the required scopes"""
    http_session = AsyncMock()
    response = AsyncMock()
    http_session.post.return_value = response
    response.json.return_value = {"access_token": "at", "scope": "read:user"}

    with pytest.raises(ValidationError):
        await logic.get_github_access_token(http_session, "code")


async def test_get_github_profile_public():
    """Test getting the user's GitHub profile"""
    http_session = AsyncMock()
    first_response = AsyncMock()

    first_response.status = 200
    first_response.json.return_value = {
        "name": "My Name",
        "email": "my@email.address",
        "id": 48
    }

    http_session.get.return_value = first_response

    profile = await get_github_profile(http_session, "token")

    assert profile.name == "My Name"
    assert profile.email == "my@email.address"

    # Verify that the second request was NOT sent:
    # mock only awaited once
    http_session.get.assert_awaited_once()
