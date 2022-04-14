from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.app.logic import editions as logic_editions
from src.app.routers.tags import Tags
from src.app.schemas.editions import EditionBase, Edition, EditionList
from src.database.database import get_session
from src.database.models import User
from .invites import invites_router
from .projects import projects_router
from .register import registration_router
from .students import students_router
from .webhooks import webhooks_router
from ...utils.dependencies import require_admin, require_auth, require_coach

# Don't add the "Editions" tag here, because then it gets applied
# to all child routes as well
editions_router = APIRouter(prefix="/editions")

# Register all child routers
child_routers = [
    invites_router, projects_router, registration_router,
    students_router, webhooks_router
]

for router in child_routers:
    # All other routes have /editions/{name} as the prefix, so they are
    # child routes of this router
    # This also means all routes have access to the "edition_name" path parameter
    editions_router.include_router(router, prefix="/{edition_name}")


@editions_router.get("/", response_model=EditionList, tags=[Tags.EDITIONS])
async def get_editions(db: Session = Depends(get_session), user: User = Depends(require_auth), page: int = 0):
    """Get a paginated list of all editions.
    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).
        user (User, optional): the current logged in user. Defaults to Depends(require_auth).
        page (int): the page to return.

    Returns:
        EditionList: an object with a list of all the editions.
    """
    if user.admin:
        return logic_editions.get_editions_page(db, page)
    else:
        return EditionList(editions=user.editions)


@editions_router.get("/{edition_name}", response_model=Edition, tags=[Tags.EDITIONS],
                     dependencies=[Depends(require_coach)])
async def get_edition_by_name(edition_name: str, db: Session = Depends(get_session)):
    """Get a specific edition.

    Args:
        edition_name (str): the name of the edition that you want to get.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).
        user (User, optional): the current logged in user. Defaults to Depends(get_current_active_user).

    Returns:
        Edition: an edition.
    """
    return logic_editions.get_edition_by_name(db, edition_name)


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


@editions_router.delete("/{edition_name}", status_code=status.HTTP_204_NO_CONTENT, tags=[Tags.EDITIONS],
                        dependencies=[Depends(require_admin)])
async def delete_edition(edition_name: str, db: Session = Depends(get_session)):
    """Delete an existing edition.

    Args:
        edition_name (str): the name of the edition that needs to be deleted, if found.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    """
    logic_editions.delete_edition(db, edition_name)
