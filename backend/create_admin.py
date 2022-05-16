"""This script is used to create the very first admin in the database

The first admin's request can't be accepted by anyone, so they have to add
themselves into the database manually.

This script does it automatically to prevent the user from having to
fiddle in the database themselves.
"""
import argparse
import asyncio
import getpass
import sys
import traceback

import sqlalchemy.exc

from src.app.exceptions.validation_exception import ValidationException
from src.database.engine import DBSession
from src.database.crud.register import create_user, create_auth_email
from src.app.logic.security import get_password_hash
from src.app.schemas.validators import validate_email_format


def get_hashed_password() -> str:
    """Let the user input their password

    This is safer than making it a command line argument, so the password
    can't be found in the history anymore

    Note: the password is NOT visible in their terminal,
    "getpass()" doesn't display the characters that you enter

    This is done twice to make sure they match, mirroring the
    frontend asking for confirmation as well
    """
    first_pass = getpass.getpass("Password: ")
    second_pass = getpass.getpass("Confirm password: ")

    # Passwords didn't match, show an error message and exit
    if first_pass != second_pass:
        print("Passwords did not match. Aborted.", file=sys.stderr)
        exit(2)

    return get_password_hash(first_pass)


async def create_admin(name: str, email: str, pw: str):
    """Create a new user in the database"""
    async with DBSession() as session:
        try:
            transaction = await session.begin_nested()
            user = await create_user(session, name, commit=False)
            user.admin = True

            # Add an email auth entry
            await create_auth_email(session, user, pw, email, commit=False)
            await session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            # Something went wrong: rollback the transaction & print the error
            await transaction.rollback()

            # Print the traceback of the exception
            print(traceback.format_exc())
            exit(3)

    await session.close()


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Add a new admin into the database.")
    parser.add_argument("-N", "--name", type=str, required=True)
    parser.add_argument("-E", "--email", type=str, required=True)

    args = parser.parse_args()

    # Check if email address was malformed
    try:
        validate_email_format(args.email)
    except ValidationException:
        print("Malformed email address. Aborted.", file=sys.stderr)
        exit(1)

    # Let user input their password
    pw_hash = get_hashed_password()

    # Create new database entry
    loop = asyncio.new_event_loop()
    loop.run_until_complete(create_admin(args.name, args.email, pw_hash))
    loop.close()

    print("Addition successful.")
