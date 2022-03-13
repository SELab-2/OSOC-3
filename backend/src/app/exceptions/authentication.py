class ExpiredCredentialsException(ValueError):
    """
    Exception raised when a user's token was valid, but has
    expired in the meantime
    A new token should be requested
    """
    pass


class InvalidCredentialsException(ValueError):
    """
    Exception raised when invalid username/password combination or
    invalid bearer token are passed as authorization credentials
    """
    pass


class UnauthorizedException(ValueError):
    """
    Exception raised when a request to a private route is made without
    a (valid) bearer token provided in the headers
    """
    pass
