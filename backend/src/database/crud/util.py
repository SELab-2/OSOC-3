from sqlalchemy.sql import Select

import settings


def paginate(query: Select, page: int) -> Select:
    """Given a query, apply pagination and return the given page based on the page size"""
    return query.slice(page * settings.DB_PAGE_SIZE, (page + 1) * settings.DB_PAGE_SIZE)
