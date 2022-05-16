from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.oauth.github import GitHubProfile
from src.database.models import AuthEmail, CoachRequest, User, Edition, AuthGitHub


async def create_user(db: AsyncSession, name: str, commit: bool = True) -> User:
    """Create a user"""
    new_user: User = User(name=name)
    db.add(new_user)

    if commit:
        await db.commit()

    return new_user


async def create_coach_request(db: AsyncSession, user: User, edition: Edition, commit: bool = True) -> CoachRequest:
    """Create a coach request"""
    coach_request: CoachRequest = CoachRequest(user=user, edition=edition)
    db.add(coach_request)

    if commit:
        await db.commit()

    return coach_request


async def create_auth_email(db: AsyncSession, user: User, pw_hash: str, email: str, commit: bool = True) -> AuthEmail:
    """Create an authentication entry for email-password"""
    auth_email: AuthEmail = AuthEmail(user=user, pw_hash=pw_hash, email=email)
    db.add(auth_email)

    if commit:
        await db.commit()

    return auth_email


async def create_auth_github(db: AsyncSession, user: User, profile: GitHubProfile, commit: bool = True) -> AuthGitHub:
    """Create an authentication entry for GitHub"""
    auth_gh = AuthGitHub(user=user, access_token=profile.access_token, email=profile.email, github_user_id=profile.id)
    db.add(auth_gh)

    if commit:
        await db.commit()

    return auth_gh
