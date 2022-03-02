from alembic import config
from alembic import script
from alembic.runtime import migration
from fastapi import FastAPI

from src.database.engine import engine
from .routers import base_router

# Main application
app = FastAPI()

# Include all routers
app.include_router(base_router)


@app.on_event('startup')
async def startup():
    alembic_config: config.Config = config.Config('alembic.ini')
    alembic_script: script.ScriptDirectory = script.ScriptDirectory.from_config(alembic_config)
    with engine.begin() as conn:
        context: migration.MigrationContext = migration.MigrationContext.configure(conn)
        if context.get_current_revision() != alembic_script.get_current_head():
            raise Exception('Pending migrations')
