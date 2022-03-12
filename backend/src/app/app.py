from alembic import config
from alembic import script
from alembic.runtime import migration
from fastapi import FastAPI, APIRouter

from src.database.engine import engine
from src.database.exceptions import PendingMigrationsException
from .routers import editions_router
from .routers.skills import skills_router
from .exceptions import install_handlers

# Main application
app = FastAPI(
    title="OSOC Team 3",
    version="0.0.1"
)

# Include all routers
app.include_router(editions_router)
app.include_router(skills_router)

# Install exception handlers
install_handlers(app)


@app.on_event('startup')
async def startup():
    """
    Check if all migrations have been executed. If not refuse to start the app.
    """
    alembic_config: config.Config = config.Config('alembic.ini')
    alembic_script: script.ScriptDirectory = script.ScriptDirectory.from_config(alembic_config)
    with engine.begin() as conn:
        context: migration.MigrationContext = migration.MigrationContext.configure(conn)
        if context.get_current_revision() != alembic_script.get_current_head():
            raise PendingMigrationsException('Pending migrations')
