from sqlalchemy.orm import Query

import settings


def paginate(query: Query, page: int) -> Query:
    return query.slice(page * settings.DB_PAGE_SIZE, (page + 1) * settings.DB_PAGE_SIZE)
