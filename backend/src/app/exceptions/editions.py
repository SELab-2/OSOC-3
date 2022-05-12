class DuplicateInsertException(Exception):
    """Exception raised when an element is inserted twice

    Args:
        Exception (Exception): base Exception class
    """


class ReadOnlyEditionException(Exception):
    """Exception raised when a read-only edition is being changed"""
