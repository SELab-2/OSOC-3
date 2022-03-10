import enum


class Tags(enum.Enum):
    """
    Enum containing the tags that can be passed to the routers.

    Helps to structure the API in the documentation.
    """
    EDITIONS = "editions"
    INVITES = "invites"
    LOGIN = "login"
    PROJECTS = "projects"
    REGISTRATION = "registration"
    SKILLS = "skills"
    STUDENTS = "students"
    USERS = "users"
