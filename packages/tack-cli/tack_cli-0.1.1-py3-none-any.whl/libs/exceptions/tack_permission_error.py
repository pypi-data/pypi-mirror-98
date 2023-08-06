from .base_error import BaseError


class TackPermissionError(BaseError):
    """A Permission error that returns a specific error code."""
    @property
    def error_code(self):
        return 51
