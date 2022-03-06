import sqlalchemy.exc
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def install_handlers(app: FastAPI):
    """Install all custom exception handlers"""

    @app.exception_handler(sqlalchemy.exc.NoResultFound)
    def sqlalchemy_exc_no_result_found(_request: Request, _exception: sqlalchemy.exc.NoResultFound):
        return JSONResponse(
            status_code=404,
            content={'message': 'Not Found'}
        )
