class StudentInConflictException(Exception):
    """
    Exception raised when a project_role of a student can't be confirmed because they are part of a conflict
    """


class FailedToAddProjectRoleException(Exception):
    """
    Exception raised when a project_role can't be added for some reason
    """


class NoStrictlyPositiveNumberOfSlots(Exception):
    """Exception raised when roles aren't strictly positive"""
