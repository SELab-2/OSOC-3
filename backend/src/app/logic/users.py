from sqlalchemy.ext.asyncio import AsyncSession

import src.database.crud.users as users_crud
from src.app.schemas.users import UsersListResponse, AdminPatch, UserRequestsResponse, user_model_to_schema, \
    FilterParameters, UserRequest
from src.database.models import User, Edition


async def get_users_list(
        db: AsyncSession,
        params: FilterParameters
) -> UsersListResponse:
    """
    Query the database for a list of users
    and wrap the result in a pydantic model
    """

    users_orm = await users_crud.get_users_filtered_page(db, params)

    return UsersListResponse(users=[user_model_to_schema(user) for user in users_orm])


async def get_user_editions(db: AsyncSession, user: User) -> list[Edition]:
    """Get all names of the editions this user is coach in"""
    return await users_crud.get_user_editions(db, user)


async def edit_admin_status(db: AsyncSession, user_id: int, admin: AdminPatch):
    """
    Edit the admin-status of a user
    """
    await users_crud.edit_admin_status(db, user_id, admin.admin)


async def add_coach(db: AsyncSession, user_id: int, edition_name: str):
    """
    Add user as coach for the given edition
    """
    await users_crud.add_coach(db, user_id, edition_name)
    await users_crud.remove_request_if_exists(db, user_id, edition_name)


async def remove_coach(db: AsyncSession, user_id: int, edition_name: str):
    """
    Remove user as coach for the given edition
    """
    await users_crud.remove_coach(db, user_id, edition_name)


async def remove_coach_all_editions(db: AsyncSession, user_id: int):
    """
    Remove user as coach from all editions
    """
    await users_crud.remove_coach_all_editions(db, user_id)


async def get_request_list(db: AsyncSession, edition_name: str | None, user_name: str | None, page: int) \
        -> UserRequestsResponse:
    """
    Query the database for a list of all user requests
    and wrap the result in a pydantic model
    """

    if user_name is None:
        user_name = ""

    if edition_name is None:
        requests = await users_crud.get_requests_page(db, page, user_name)
    else:
        requests = await users_crud.get_requests_for_edition_page(db, edition_name, page, user_name)

    requests_model = []
    for request in requests:
        user_req = UserRequest(request_id=request.request_id, edition=request.edition,
                               user=user_model_to_schema(request.user))
        requests_model.append(user_req)
    return UserRequestsResponse(requests=requests_model)


async def accept_request(db: AsyncSession, request_id: int):
    """
    Accept user request
    """
    await users_crud.accept_request(db, request_id)


async def reject_request(db: AsyncSession, request_id: int):
    """
    Reject user request
    """
    await users_crud.reject_request(db, request_id)
