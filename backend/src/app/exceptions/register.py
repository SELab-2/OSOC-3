class FailedToAddNewUserException(Exception):
    """
    Exception raised when a new user can't be added
    """


class InvalidGitHubCode(Exception):
    """Exception raised when a GitHub auth code is invalid or has expired"""
