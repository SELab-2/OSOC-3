from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
from src.app.schemas.editions import EditionBase, Edition, EditionList

from src.database.database import get_session
from src.app.logic import editions as logic_editions

from .invites import invites_router
from .projects import projects_router
from .register import registration_router
from .students import students_router
from .webhooks import webhooks_router

# Don't add the "Editions" tag here, because then it gets applied
# to all child routes as well
from ...utils.dependencies import require_admin, require_auth, require_coach

editions_router = APIRouter(prefix="/editions")

# Register all child routers
child_routers = [
    invites_router, projects_router, registration_router,
    students_router, webhooks_router
]

for router in child_routers:
    # All other routes have /editions/{id} as the prefix, so they are
    # child routes of this router
    # This also means all routes have access to the "edition_id" path parameter
    editions_router.include_router(router, prefix="/{edition_id}")


@editions_router.get("/", response_model=EditionList, tags=[Tags.EDITIONS], dependencies=[Depends(require_auth)])
async def get_editions(db: Session = Depends(get_session)):
    """Get a list of all editions.
    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        EditionList: an object with a list of all the editions.
    """
    # TO DO only return editions the user can see
    return logic_editions.get_editions(db)


@editions_router.get("/{edition_id}", response_model=Edition, tags=[Tags.EDITIONS],
                     dependencies=[Depends(require_coach)])
async def get_edition_by_id(edition_id: int, db: Session = Depends(get_session)):
    """Get a specific edition.

    Args:
        edition_id (int): the id of the edition that you want to get.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        Edition: an edition.
    """
    return logic_editions.get_edition_by_id(db, edition_id)


@editions_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Edition, tags=[Tags.EDITIONS],
                      dependencies=[Depends(require_admin)])
async def post_edition(edition: EditionBase, db: Session = Depends(get_session)):
    """ Create a new edition.

    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        Edition: the newly made edition object.
    """
    return logic_editions.create_edition(db, edition)


@editions_router.delete("/{edition_id}", status_code=status.HTTP_204_NO_CONTENT, tags=[Tags.EDITIONS],
                        dependencies=[Depends(require_admin)])
async def delete_edition(edition_id: int, db: Session = Depends(get_session)):
    """Delete an existing edition.

    Args:
        edition_id (int): the id of the edition that needs to be deleted, if found.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    """
    logic_editions.delete_edition(db, edition_id)
