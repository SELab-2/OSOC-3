class ExpiredCredentialsException(ValueError):
    """
    Exception raised when a user's token was valid, but has
    expired in the meantime
    A new token should be requested
    """


class InvalidCredentialsException(ValueError):
    """
    Exception raised when invalid username/password combination or
    invalid bearer token are passed as authorization credentials
    """


class MissingPermissionsException(ValueError):
    """
    Exception raised when a request to a private route is made without
    a (valid) bearer token provided in the headers

    Also raised when a coach tries to make a request to a route
    when their application is still pending, and they haven't been
    accepted yet
    """


class WrongTokenTypeException(ValueError):
    """
    Exception raised when a request to a private route is made with a
    valid jwt token, but a wrong token type. eg: trying to authenticate
    using a refresh token
    """