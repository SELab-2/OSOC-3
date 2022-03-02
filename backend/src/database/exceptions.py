class PendingMigrationsException(Exception):
    """
    Exception indication the database is not yet fully migrated.
    """
    pass
