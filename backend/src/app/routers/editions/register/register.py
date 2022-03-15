from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.app.logic.register import create_request
from src.app.routers.tags import Tags
from src.app.schemas.register import NewUser
from src.app.utils.dependencies import get_edition
from src.database.database import get_session
from src.database.models import Edition

registration_router = APIRouter(prefix="/register", tags=[Tags.REGISTRATION])


@registration_router.post("/email", status_code=status.HTTP_201_CREATED)
async def register_email(user: NewUser, db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Register a new account using the email/password format.
    """
    create_request(db, user, edition)
