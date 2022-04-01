class StudentInConflictException(Exception):
    """
    Exception raised when a project_role of a student can't be confirmed because they are part of a conflict
    """


class FailedToAddProjectRoleException(Exception):
    """
    Exception raised when a projct_role can't be added for some reason
    """
