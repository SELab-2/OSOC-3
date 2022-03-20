from typing import Any

from environs import Env
import enum


env = Env()

# Read the .env file
env.read_env()

"""API"""
# Allowed origins (CORS)
CORS_ORIGINS: list[str] = env.list("CORS_ORIGINS", ["http://localhost:3000"])

"""Database"""
# Name of the database
DB_NAME: str = env.str("DB_NAME", "osoc_dev")
# Username used to log in
DB_USERNAME: str = env.str("DB_USER", "root")
# Password used to log in
DB_PASSWORD: str = env.str("DB_PASSWORD", "password")
# IP-address the database is running on
DB_HOST: str = env.str("DB_HOST", "0.0.0.0")
# Port the database is running on
DB_PORT: int = env.int("DB_PORT", 3306)
# Option to change te database used. Default False is Mariadb.
DB_USE_SQLITE: bool = env.bool("DB_USE_SQLITE", False)

"""JWT token key"""
SECRET_KEY: str = env.str("SECRET_KEY", "4d16a9cc83d74144322e893c879b5f639088c15dc1606b11226abbd7e97f5ee5")


@enum.unique
class FormMapping(enum.Enum):
    FIRST_NAME = "question_3ExXkL"
    LAST_NAME = "question_nro6jL"
    PREFERRED_NAME_OPTION = "question_w4K84o"
    PREFERRED_NAME = "question_3jlya9"
    EMAIL = "question_nW8NOQ"
    PHONE_NUMBER = "question_mea6qo"
    #CV = "question_wa26Qy"
    STUDENT_COACH = "question_wz7qEE"

    UNKNOWN = None  # Returned when no specific question can be matched

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return FormMapping.UNKNOWN
