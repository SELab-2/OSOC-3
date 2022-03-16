import sqlalchemy.exc
from .editions import DuplicateInsertException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status


def install_handlers(app: FastAPI):
    """Install all custom exception handlers"""

    @app.exception_handler(sqlalchemy.exc.NoResultFound)
    def sqlalchemy_exc_no_result_found(_request: Request, _exception: sqlalchemy.exc.NoResultFound):
        return JSONResponse(
            status_code=404,
            content={'message': 'Not Found'}
        )

    @app.exception_handler(DuplicateInsertException)
    def duplicate_insert(_request: Request, _exception: DuplicateInsertException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Already inserted'}
        )
