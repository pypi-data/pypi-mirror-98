import hashlib

from .base_hash import BaseHash


class Sha256(BaseHash):
    """Handles SHA256 hashes"""
    def __init__(self):
        super().__init__(hashlib.sha256())

    def update(self, text):
        """
        Updates the hash with new input data (payload)
        :param text: The payload to be hashed.
        :return: None
        """
        self._algorithm.update(text)

    def hexdigest(self):
        """
        Creates a hexadecimal digest from the hash.
        :return: Returns the string (if implemented)
        """
        return f'0x{self._algorithm.hexdigest()}'
