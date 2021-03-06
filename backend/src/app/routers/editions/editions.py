from asyncio import Queue

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response
from websockets.exceptions import ConnectionClosedOK

from src.app.logic import editions as logic_editions
from src.app.routers.tags import Tags
from src.app.schemas.editions import EditionBase, Edition, EditionList, EditEdition
from src.database.database import get_session
from src.database.models import User, Edition as EditionDB
from .invites import invites_router
from .projects import projects_router
from .register import registration_router
from .students import students_router
from .webhooks import webhooks_router
from ...utils.dependencies import require_admin, require_auth, require_coach, require_coach_ws, get_edition
from ...utils.websockets import DataPublisher, get_publisher

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


@editions_router.get("", response_model=EditionList, tags=[Tags.EDITIONS])
async def get_editions(db: AsyncSession = Depends(get_session), user: User = Depends(require_auth), page: int = 0):
    """Get a paginated list of all editions."""
    if user.admin:
        return await logic_editions.get_editions_page(db, page)

    return EditionList(editions=user.editions)


@editions_router.patch("/{edition_name}", response_class=Response, tags=[Tags.EDITIONS],
                       dependencies=[Depends(require_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def patch_edition(edit_edition: EditEdition, edition: EditionDB = Depends(get_edition),
                        db: AsyncSession = Depends(get_session)):
    """Change the readonly status of an edition
    Note that this route is not behind "get_editable_edition", because otherwise you'd never be able
    to change the status back to False
    """
    await logic_editions.patch_edition(db, edition, edit_edition.readonly)


@editions_router.get(
    "/{edition_name}",
    response_model=Edition,
    tags=[Tags.EDITIONS],
    dependencies=[Depends(require_coach)]
)
async def get_edition_by_name(edition_name: str, db: AsyncSession = Depends(get_session)):
    """Get a specific edition."""
    return await logic_editions.get_edition_by_name(db, edition_name)


@editions_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Edition,
    tags=[Tags.EDITIONS],
    dependencies=[Depends(require_admin)]
)
async def post_edition(edition: EditionBase, db: AsyncSession = Depends(get_session)):
    """ Create a new edition."""
    return await logic_editions.create_edition(db, edition)


@editions_router.delete(
    "/{edition_name}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    tags=[Tags.EDITIONS],
    dependencies=[Depends(require_admin)]
)
async def delete_edition(edition_name: str, db: AsyncSession = Depends(get_session)):
    """Delete an existing edition."""
    await logic_editions.delete_edition(db, edition_name)


@editions_router.websocket('/{edition_name}/live')
async def feed(
        websocket: WebSocket,
        publisher: DataPublisher = Depends(get_publisher),
        _: User = Depends(require_coach_ws)
):
    """Handle websocket.
    Events in the application are sent using this websocket
    """
    await websocket.accept()
    queue: Queue = await publisher.subscribe()
    try:
        while True:
            data: dict = await queue.get()
            await websocket.send_json(data)
    except ConnectionClosedOK:
        pass
    finally:
        await publisher.unsubscribe(queue)
