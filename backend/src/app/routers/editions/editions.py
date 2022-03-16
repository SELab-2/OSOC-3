from fastapi import APIRouter

from src.app.routers.tags import Tags

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


@editions_router.get("/", tags=[Tags.EDITIONS])
async def get_editions():
    """
    Get a list of all editions.
    """


@editions_router.post("/", tags=[Tags.EDITIONS])
async def post_edition():
    """
    Create a new edition.
    """


@editions_router.delete("/{edition_id}", tags=[Tags.EDITIONS])
async def delete_edition(edition_id: int):
    """
    Delete an existing edition.
    """
