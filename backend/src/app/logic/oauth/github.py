import aiohttp
from starlette import status

from src.app.exceptions.register import InvalidGitHubCode
from src.app.schemas.oauth.github import AccessTokenResponse, GitHubProfile
import settings


async def get_github_access_token(session: aiohttp.ClientSession, code: str) -> AccessTokenResponse:
    """Get a user's GitHub access token"""
    headers = {
        # Explicitly request the V3 API as recommended in the docs:
        # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current-version
        "Accept": "application/vnd.github.v3+json"
    }

    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code
    }

    token_response = await session.post("https://github.com/login/oauth/access_token", headers=headers, params=params)
    token_response_json = await token_response.json()

    # For some reason this endpoint responds with a 200 if something is wrong so we have to check
    # the fields in the body
    if "error" in token_response_json:
        raise InvalidGitHubCode(token_response_json["error_description"])

    return AccessTokenResponse(**token_response_json)


async def get_github_email(session: aiohttp.ClientSession, access_token: str) -> GitHubProfile:
    """Get a user's profile info used on GitHub"""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    profile = await session.get("https://api.github.com/user", headers=headers)
    profile_json = await profile.json()

    assert profile.status == status.HTTP_200_OK, profile_json

    # Default to GH name if real name is not available
    name = profile_json.get("name", None) or profile_json.get("login")
    email = profile_json.get("email", None)

    # Email can be private, in which case we have to send another request
    # to access all their other emails
    if email is None:
        user_emails = await session.get("https://api.github.com/user/emails", headers=headers)
        user_emails_json = await user_emails.json()

        assert user_emails.status == status.HTTP_200_OK, user_emails_json

        # Find primary email
        for private_email in user_emails_json:
            if private_email["primary"]:
                email = private_email["email"]
                break

        # No primary email set, take the first email address from the list
        # (no idea if this is possible, but better safe than sorry)
        if email is None:
            email = user_emails_json[0]["email"]

    return GitHubProfile(access_token=access_token, email=email, name=name)
