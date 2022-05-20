import asyncio
import traceback
from argparse import ArgumentParser

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

import src.app  # Important import - avoids circular import
from src.database.crud import editions
from src.database.crud.webhooks import create_webhook
from src.database.engine import DBSession
from src.database.models import Edition, WebhookURL


async def do(args):
    session: AsyncSession
    async with DBSession() as session:
        try:
            edition: Edition = await editions.get_edition_by_name(session, args.edition)
            webhook_url: WebhookURL = await create_webhook(session, edition)
            print(f'WebhookURL created: {webhook_url.uuid}')
        except sqlalchemy.exc.SQLAlchemyError:
            await session.rollback()
            print(traceback.format_exc())
            exit(3)


if __name__ == '__main__':
    parser = ArgumentParser(description="Add new webhook to edition.")
    parser.add_argument("-E", "--edition", type=str, required=True)
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(do(args))
    loop.close()
