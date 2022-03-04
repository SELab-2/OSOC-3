from environs import Env


env = Env()

# Read the .env file
env.read_env()

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
