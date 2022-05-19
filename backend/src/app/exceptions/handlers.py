import sqlalchemy.exc
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

from .authentication import (
    ExpiredCredentialsException, InvalidCredentialsException,
    MissingPermissionsException, WrongTokenTypeException)
from .crud import DuplicateInsertException
from .editions import ReadOnlyEditionException
from .parsing import MalformedUUIDError
from .projects import StudentInConflictException, FailedToAddProjectRoleException, NoneStrictPostiveNumberOfSlots
from .register import FailedToAddNewUserException, InvalidGitHubCode
from .students_email import FailedToAddNewEmailException
from .webhooks import WebhookProcessException
from .util import NotFound


# Pylint says there are too many local variables because of all the inner functions here
# however, we can't really change that so we'll just disable the warning because it doesn't make
# a lot of sense
# pylint: disable=R0914
def install_handlers(app: FastAPI):
    """Install all custom exception handlers"""

    @app.exception_handler(ExpiredCredentialsException)
    def expired_credentials(_request: Request, _exception: ExpiredCredentialsException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Credentials expired"},
        )

    @app.exception_handler(InvalidCredentialsException)
    def invalid_credentials(_request: Request, _exception: InvalidCredentialsException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InvalidGitHubCode)
    def invalid_github_code(_request: Request, _exception: InvalidGitHubCode):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(_exception)}
        )

    @app.exception_handler(MalformedUUIDError)
    def malformed_uuid_error(_request: Request, _exception: MalformedUUIDError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": f"Malformed UUID: {str(_exception)}"}
        )

    @app.exception_handler(MissingPermissionsException)
    def missing_permissions(_request: Request, _exception: MissingPermissionsException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "You don't have permission to perform this action."}
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

    @app.exception_handler(NotFound)
    def not_found(_request: Request, _exception: NotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'Not Found'}
        )

    @app.exception_handler(DuplicateInsertException)
    def duplicate_insert(_request: Request, _exception: DuplicateInsertException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Already inserted'}
        )

    @app.exception_handler(WebhookProcessException)
    def webhook_process_exception(_request: Request, exception: WebhookProcessException):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={'message': exception.message}
        )

    @app.exception_handler(FailedToAddNewUserException)
    def failed_to_add_new_user_exception(_request: Request, _exception: FailedToAddNewUserException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Something went wrong while creating a new user'}
        )

    @app.exception_handler(StudentInConflictException)
    def student_in_conflict_exception(_request: Request, _exception: StudentInConflictException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'message': 'Resolve the conflict this student is in before confirming their role'}
        )

    @app.exception_handler(FailedToAddProjectRoleException)
    def failed_to_add_project_role_exception(_request: Request, _exception: FailedToAddProjectRoleException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'message': 'Something went wrong while adding this student to the project'}
        )

    @app.exception_handler(WrongTokenTypeException)
    async def wrong_token_type_exception(_request: Request, _exception: WrongTokenTypeException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'message': 'You used the wrong token to access this resource.'}
        )

    @app.exception_handler(ReadOnlyEditionException)
    def read_only_edition_exception(_request: Request, _exception: ReadOnlyEditionException):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={'message': 'This edition is Read-Only'}
        )

    @app.exception_handler(FailedToAddNewEmailException)
    def failed_to_add_new_email_exception(_request: Request, _exception: FailedToAddNewEmailException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Something went wrong while creating a new email'}
        )

    @app.exception_handler(NoneStrictPostiveNumberOfSlots)
    def none_strict_postive_number_of_slots(_request: Request, _exception: NoneStrictPostiveNumberOfSlots):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={'message': 'Roles has to be strict positive'}
        )
