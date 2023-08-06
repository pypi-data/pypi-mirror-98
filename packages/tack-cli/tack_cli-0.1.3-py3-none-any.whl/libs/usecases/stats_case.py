import os

import libs.constants as constants
from libs.common.timeit import timeit


# pylint: disable=too-few-public-methods
class StatsCase:
    """
    Stats use-case for returning statistics.
    """
    def __init__(self, storage_service, tack_meta_service, reporting_service):
        self.storage_service = storage_service
        self.tack_meta_service = tack_meta_service
        self.reporting_service = reporting_service

    @timeit
    async def action_stats(self, directory):
        """
        Handles the gathering and showing of the stats
        :param directory: The directory is used to specify the repository.
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)
        database = await self.storage_service.stats(directory)
        db_path = os.path.join(repo.path, constants.repository_storage)
        stat_obj = os.stat(db_path)
        structure_to_print = {
            'type': 'stats',
            'repository': {
                'path': repo.path,
                'config': repo.config,
            },
            'database': database
        }
        structure_to_print['database']['size'] = stat_obj.st_size

        return self.reporting_service.print(structure_to_print)
