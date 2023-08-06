from .base_error import BaseError


class TackRepositoryNotFoundError(BaseError):
    """Not found error class."""
    @property
    def error_code(self):
        return 50
