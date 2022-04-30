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


async def test_get_github_profile_public_email():
    """Test getting the user's GitHub profile when the email is public"""
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


async def test_get_github_profile_no_name_uses_login():
    """Test getting the user's GitHub profile when the name is None"""
    http_session = AsyncMock()
    first_response = AsyncMock()

    first_response.status = 200
    first_response.json.return_value = {
        "name": None,
        "email": "my@email.address",
        "login": "login",
        "id": 48
    }

    http_session.get.return_value = first_response

    profile = await get_github_profile(http_session, "token")

    assert profile.name == "login"


async def test_get_github_profile_private_email():
    """Test getting a user's GitHub profile when their email address is private"""
    http_session = AsyncMock()
    first_response = AsyncMock()

    first_response.status = 200
    first_response.json.return_value = {
        "name": "My Name",
        "email": None,
        "id": 48
    }

    second_response = AsyncMock()
    second_response.status = 200
    second_response.json.return_value = [
        {
            "primary": False, "email": "secondary@email.com"
        },
        {
            "primary": True, "email": "primary@email.com"
         }
    ]

    http_session.get.side_effect = [first_response, second_response]

    profile = await get_github_profile(http_session, "token")

    # Primary email was used
    assert profile.email == "primary@email.com"
    assert http_session.get.await_count == 2


async def test_get_github_profile_no_primary_email():
    """Test getting a user's GitHub profile when they have no primary email set
    Not sure if this is possible but better safe than sorry
    """
    http_session = AsyncMock()
    first_response = AsyncMock()

    first_response.status = 200
    first_response.json.return_value = {
        "name": "My Name",
        "email": None,
        "id": 48
    }

    second_response = AsyncMock()
    second_response.status = 200
    second_response.json.return_value = [
        {
            "primary": False, "email": "secondary@email.com"
        },
        {
            "primary": False, "email": "primary@email.com"
         }
    ]

    http_session.get.side_effect = [first_response, second_response]

    profile = await get_github_profile(http_session, "token")

    # No primary email, this should now default to the first entry in the list
    assert profile.email == "secondary@email.com"
    assert http_session.get.await_count == 2
