class BaseError(Exception):
    """
    The base error class that introduces additional properties and attributes.
    """
    @property
    def error_code(self):
        """
        Returns the unique error code that might be served as exit code.
        :return: The error code
        """
        return 1
