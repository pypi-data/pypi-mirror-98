import libs.common.timeit as timeit


class InitCase:
    """Use case to handle initializations of a repository"""

    def __init__(self, tack_meta_service, reporting_service):
        self.tack_meta_service = tack_meta_service
        self.reporting_service = reporting_service

    @timeit.timeit
    async def action_init(self, directory):
        """
        Initializes a new repository at the given directory.
        :param directory: The location where you want to create a new repository.
        :return: None
        """
        is_new_repository, target_folder = await self.tack_meta_service.create_repository(directory)

        structure_to_print = {
            'type': 'init',
            'root': self.tack_meta_service.get_repository(directory).path,
            'is_new_repository': is_new_repository,
            'target_folder': target_folder,
        }

        return self.reporting_service.print(structure_to_print)
