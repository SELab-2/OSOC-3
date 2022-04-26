# Urlencode the password to pass it to the engine
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import sessionmaker

import settings

engine: Engine

if settings.DB_USE_SQLITE:
    # Use sqlite database.
    engine = create_engine(URL.create(
        drivername="sqlite",
        database="test.db"
    ), connect_args={"check_same_thread": False})
else:
    # Use Mariadb database.
    _encoded_password = quote_plus(settings.DB_PASSWORD)
    engine = create_engine(URL.create(
        drivername="mariadb+mariadbconnector",
        username=settings.DB_USERNAME,
        password=_encoded_password,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    ), pool_pre_ping=True)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
