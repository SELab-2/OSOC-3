# Urlencode the password to pass it to the engine
from typing import Dict
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import sessionmaker

import settings

DATABASE_ARGS: Dict[str, str]

if settings.DB_USE_SQLITE:
    # Use sqlite database.
    DATABASE_ARGS = {
        "drivername": "sqlite",
        "database": "test.db"
    }
else:
    # Use Mariadb database.
    _encoded_password = quote_plus(settings.DB_PASSWORD)
    DATABASE_ARGS = {
        "drivername": "mariadb+mariadbconnector",
        "username": settings.DB_USERNAME,
        "password": _encoded_password,
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database": settings.DB_NAME
    }

engine: Engine = create_engine(URL.create(**DATABASE_ARGS))

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
