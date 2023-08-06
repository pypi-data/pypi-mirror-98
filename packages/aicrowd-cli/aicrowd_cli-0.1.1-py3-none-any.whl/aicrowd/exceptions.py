"""
Exceptions that the CLI raises

All other exceptions will inherit from `CLIException` so just catching that should be enough
"""

from aicrowd import errors


class CLIException(Exception):
    """
    Base class for all exceptions raised by CLI
    """

    def __init__(
        self, message: str, fix: str = None, exit_code: int = errors.UNKNOWN_ERROR
    ):
        """
        Args:
            message: this will be printed to the console
            fix: (if defined) what steps can be taken to fix the error
            exit_code: what the exit code should be if this exception was raised
        """
        super().__init__(message)

        self.message = message
        self.fix = fix
        self.exit_code = exit_code

    def __repr__(self):
        return f"{type(self).__name__}\nMessage: {self.message}\nFix?: {self.fix}"
