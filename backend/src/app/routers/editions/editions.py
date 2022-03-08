from fastapi import APIRouter, Depends
from typing import List, Optional

from src.app.routers.tags import Tags

from src.database.database import get_session
from src.database.schemas import EditionBase, Edition
from src.database.crud import editions as crud_editions
from sqlalchemy.orm import Session

from .invites import invites_router
from .projects import projects_router
from .register import registration_router
from .skills import skills_router
from .students import students_router
from .users import users_router
from .webhooks import webhooks_router

# Don't add the "Editions" tag here, because then it gets applied
# to all child routes as well
editions_router = APIRouter(prefix="/editions")

# Register all child routers
child_routers = [
    invites_router, projects_router, registration_router,
    skills_router, students_router, users_router,
    webhooks_router
]

for router in child_routers:
    # All other routes have /editions/{id} as the prefix, so they are
    # child routes of this router
    # This also means all routes have access to the "edition_id" path parameter
    editions_router.include_router(router, prefix="/{edition_id}")


@editions_router.get("/",response_model=list[Edition], tags=[Tags.EDITIONS])
async def get_editions(db: Session = Depends(get_session)):
    """Get a list of all editions.

    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        List[Edition]: a list of all the editions.
    """
    return crud_editions.get_editions(db)


@editions_router.get("/{edition_id}",response_model=Edition | None, tags=[Tags.EDITIONS])
async def get_editions_by_id(edition_id: int, db: Session = Depends(get_session)):
    """Get a specific edition.

    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        Edition: an edition
    """
    return crud_editions.get_edition_by_key(db, edition_id)


@editions_router.post("/",response_model=Edition, tags=[Tags.EDITIONS])
async def post_edition(edition: EditionBase, db: Session = Depends(get_session)):
    """ Create a new edition.

    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        Edition: the newly made edition object.
    """
    return crud_editions.create_edition(db, edition)


@editions_router.delete("/{edition_id}", tags=[Tags.EDITIONS])
async def delete_edition(edition_id: int, db: Session = Depends(get_session)):
    """Delete an existing edition.

    Args:
        edition_id (int): the id of the edition that needs to be deleted, if found.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns: nothing
    """
    crud_editions.delete_edition(db, edition_id)
