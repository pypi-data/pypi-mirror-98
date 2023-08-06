import zlib

from .base_hash import BaseHash


class Crc32(BaseHash):
    """Handles CRC32 hashes"""
    def __init__(self):
        self._previous = 0
        super().__init__(None)

    def update(self, text):
        """
        Updates the hash with new input data (payload)
        :param text: The payload to be hashed.
        :return: None
        """
        self._previous = zlib.crc32(text, self._previous)

    def hexdigest(self):
        """
        Creates a hexadecimal digest from the hash.
        :return: Returns the string (if implemented)
        """
        return hex(self._previous & 0xffffffff)
