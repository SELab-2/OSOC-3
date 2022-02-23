from fastapi import FastAPI
from .routers import base_router


# Main application
app = FastAPI()

# Include all routers
app.include_router(base_router)
