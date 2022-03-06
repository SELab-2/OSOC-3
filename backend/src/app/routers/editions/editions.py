from fastapi import APIRouter, Depends

from src.app.routers.tags import Tags

from fastapi import Depends
from src.database.database import get_session
from src.database.models import Edition
from sqlalchemy.orm import Session

from .invites import invites_router
from .projects import projects_router
from .register import registration_router
from .skills import skills_router
from .students import students_router
from .users import users_router

# Don't add the "Editions" tag here, because then it gets applied
# to all child routes as well
editions_router = APIRouter(prefix="/editions")

# Register all child routers
child_routers = [
    invites_router, projects_router, registration_router,
    skills_router, students_router, users_router
]

for router in child_routers:
    # All other routes have /editions/{id} as the prefix, so they are
    # child routes of this router
    # This also means all routes have access to the "edition_id" path parameter
    editions_router.include_router(router, prefix="/{edition_id}")


@editions_router.get("/", tags=[Tags.EDITIONS])
async def get_editions(db: Session = Depends(get_session)):
    """
    Get a list of all editions.
    """
    return db.query(Edition).all()



@editions_router.post("/", tags=[Tags.EDITIONS])
async def post_edition(db: Session = Depends(get_session)):
    """
    Create a new edition.
    """
    new_edition: Edition = Edition()
    new_edition.year = 2022
    db.add(new_edition)
    db.commit()
    db.refresh(new_edition)
    return new_edition



@editions_router.delete("/{edition_id}", tags=[Tags.EDITIONS])
async def delete_edition(edition_id: int, db: Session = Depends(get_session)):
    """
    Delete an existing edition.
    """
    edition: Edition = db.get(Edition, edition_id)
    db.delete(edition)
    db.commit()
    return {"data": "ok"}

    
    
