from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AuthEmail, CoachRequest, User, Edition


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
    """Create a authentication for email"""
    auth_email: AuthEmail = AuthEmail(user=user, pw_hash=pw_hash, email=email)
    db.add(auth_email)

    if commit:
        await db.commit()

    return auth_email
