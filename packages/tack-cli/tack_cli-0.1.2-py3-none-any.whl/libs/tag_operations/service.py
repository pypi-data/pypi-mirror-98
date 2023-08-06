from libs.common.timeit import timeit


class Service:
    """The service is used to proxy the repository"""

    def __init__(self, repository):
        self.repository = repository

    @timeit
    async def find_files(self, directory, ignored_matches):
        """
        Finds files in a specified directory.
        :param directory: Any sub path in the repository.
        :param ignored_matches: The ignore rules
        :return: Returns an array with found files.
        """
        return await self.repository.find_files(directory, ignored_matches)

    @timeit
    async def fingerprint_files(self, directory, file_data_objects):
        """
        Finger prints the previously found files.
        :param directory: Any sub path in the repository.
        :param file_data_objects: The file objects to be iterated upon.
        :return: Returns a set with the generated fingerprint.
        """
        return await self.repository.fingerprint_files(directory, file_data_objects)
