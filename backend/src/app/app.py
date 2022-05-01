from alembic import config
from alembic import script
from alembic.runtime import migration
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import settings
from src.database.engine import engine
from src.database.exceptions import PendingMigrationsException
from .exceptions import install_handlers
from .routers import editions_router, login_router, skills_router
from .routers.users.users import users_router

# Main application
app = FastAPI(
    title="OSOC Team 3",
    version="0.0.1"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(editions_router)
app.include_router(skills_router)
app.include_router(login_router)
app.include_router(users_router)

# Install exception handlers
install_handlers(app)


@app.on_event('startup')
async def startup():
    """
    Check if all migrations have been executed. If not refuse to start the app.
    """
    alembic_config: config.Config = config.Config('alembic.ini')
    alembic_script: script.ScriptDirectory = script.ScriptDirectory.from_config(alembic_config)
    async with engine.begin() as conn:
        revision: str = await conn.run_sync(
            lambda sync_conn: migration.MigrationContext.configure(sync_conn).get_current_revision()
        )
        alembic_head: str = alembic_script.get_current_head()
        if revision != alembic_head:
            raise PendingMigrationsException('Pending migrations')
