import sqlalchemy.exc
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

from .parsing import MalformedUUIDError
from .webhooks import WebhookProcessException


def install_handlers(app: FastAPI):
    """Install all custom exception handlers"""

    @app.exception_handler(MalformedUUIDError)
    def malformed_uuid_error(_request: Request, _exception: MalformedUUIDError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": f"Malformed UUID: {str(_exception)}"}
        )

    # Note: pydantic validation raises a pydantic.ValidationError when validation fails,
    # so it's not possible to catch our own custom ValidationException here!
    @app.exception_handler(ValidationError)
    def validation_exception(_request: Request, _exception: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(_exception)}
        )

    @app.exception_handler(sqlalchemy.exc.NoResultFound)
    def sqlalchemy_exc_no_result_found(_request: Request, _exception: sqlalchemy.exc.NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'Not Found'}
        )

    @app.exception_handler(WebhookProcessException)
    def webhook_process_exception(_request: Request, exception: WebhookProcessException):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={'message': exception.message}
        )
