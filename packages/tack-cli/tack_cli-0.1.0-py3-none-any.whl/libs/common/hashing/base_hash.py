from abc import abstractmethod, ABC

import aiofiles


class BaseHash(ABC):
    """The base class to manufacture a nice hash"""
    def __init__(self, algorithm = None):
        self._algorithm = algorithm

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        pass

    @abstractmethod
    def hexdigest(self):
        """
        Creates a hexadecimal digest from the hash.
        :return: Returns the string (if implemented)
        """

    @abstractmethod
    def update(self, text):
        """
        Updates the hash with new input data (payload)
        :param text: The payload to be hashed.
        :return: None
        """

    @classmethod
    async def hash_file(cls, file_path):
        """
        Hashes a file at the given location in an asynchronous manner.
        :param file_path: The file path to be read.
        :return: Returns the hex digest of the entire file.
        """
        async with aiofiles.open(file_path, 'rb') as file:
            with cls() as hash_obj:
                while chunk := await file.read(8192):
                    hash_obj.update(chunk)
                return hash_obj.hexdigest()
