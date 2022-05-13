# Urlencode the password to pass it to the engine
from urllib.parse import quote_plus

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

engine: AsyncEngine

if settings.DB_USE_SQLITE:
    # Use sqlite database.
    engine = create_async_engine(URL.create(
        drivername="sqlite+aiosqlite",
        database="test.db"
    ), connect_args={"check_same_thread": False})
else:
    # Use Mariadb database.
    _encoded_password = quote_plus(settings.DB_PASSWORD)
    engine = create_async_engine(URL.create(
        drivername="mariadb+asyncmy",
        username=settings.DB_USERNAME,
        password=_encoded_password,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    ), pool_pre_ping=True)

# AsyncSession needs expire_on_commit to be False
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)
