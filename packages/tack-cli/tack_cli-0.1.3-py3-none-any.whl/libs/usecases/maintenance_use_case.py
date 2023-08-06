from libs.common.timeit import timeit
from libs.tack_meta.service import TackMetaService


class MaintenanceUseCase:
    """Use case to handle maintenance operations"""
    def __init__(self, tack_meta_service: TackMetaService, reporting_service):
        self.tack_meta_service = tack_meta_service
        self.reporting_service = reporting_service

    @timeit
    async def action_setting_list(self, directory):
        """
        Lists the entire settings of the repo.
        :param directory: The directory is used to specify the repository.
        :return: Returns the list of settings
        """
        repo_hub = self.tack_meta_service.get_repository(directory)
        settings = self.tack_meta_service.get_settings(repo_hub.path)

        structure_to_print = {
            'type': 'setting_list',
            'root': repo_hub.path,
            'settings': settings
        }
        self.reporting_service.print(structure_to_print)

    @timeit
    async def action_set_setting(self, directory, opts):
        """
        Sets the key-value of a setting
        :param directory: The directory is used to specify the repository.
        :param opts: The options (key/value) of a setting.
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)
        written_config = self.tack_meta_service.set_setting(repo.path, opts)

        structure_to_print = {
            'type': 'set_setting',
            'root': repo.path,
            'config': written_config
        }

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_unset_setting(self, directory, opts):
        """
        Unsets the key of a setting.
        :param directory: The directory is used to specify the repository.
        :param opts: The options (key) of a setting.
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)
        written_config = self.tack_meta_service.unset_setting(repo.path, opts)

        structure_to_print = {
            'type': 'unset_setting',
            'root': repo.path,
            'config': written_config
        }

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_maintenance_integrity(self, directory, fix_integrity=True):
        """
        Checks and fixes the integrity of the repository
        :param directory: The directory is used to specify the repository.
        :param fix_integrity: Whether you'd like to fix the integrity or not.
        :return: None
        """
        repo_hub = self.tack_meta_service.get_repository(directory)

        calculated_integrity = await self.tack_meta_service.calculate_integrity(repo_hub.path)
        database_integrity = calculated_integrity

        integrity_in_tact = repo_hub.config.get('integrity', {}) == database_integrity

        structure_to_print = {
            'type': 'maintenance_integrity',
            'root': repo_hub.path,
            'integrity_in_tact': integrity_in_tact,
            'repo_path': repo_hub.path,
            'integrity_was_fixed': False,
            'database_integrity': database_integrity,
            'saved_integrity': repo_hub.config.get('integrity', {})
        }

        if fix_integrity and not integrity_in_tact:
            self.tack_meta_service.write_integrity(directory, database_integrity)
            structure_to_print['integrity_was_fixed'] = True

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_maintenance_matcher_list(self, directory):
        """
        Lists all the configured matchers in the repository
        :param directory: The directory is used to specify the repository.
        :return: None
        """
        ignored_matches = self.tack_meta_service.get_ignored_matches(directory)

        structure_to_print = {
            'type': 'matcher_list',
            'root': self.tack_meta_service.get_repository(directory).path,
            'ignored_matches': ignored_matches
        }

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_maintenance_matcher_add(self, directory, match):
        """
        Adds a new matcher in the repository
        :param directory: The directory is used to specify the repository.
        :param match: The match itself you want to add
        :return: None
        """
        success = self.tack_meta_service.add_to_ignored_matches(directory, match)

        structure_to_print = {
            'type': 'matcher_add',
            'root': self.tack_meta_service.get_repository(directory).path,
            'match': match,
            'success': success
        }

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_maintenance_matcher_remove(self, directory, match):
        """
        Removes a specific matcher from the repository
        :param directory: The directory is used to specify the repository.
        :param match: The match to find and remove
        :return: None
        """
        success, delete_confirmation = self.tack_meta_service.delete_from_ignored_matches(directory, match)

        structure_to_print = {
            'type': 'matcher_remove',
            'root': self.tack_meta_service.get_repository(directory).path,
            'match': match,
            'success': success,
            'delete_confirmation': delete_confirmation
        }

        return self.reporting_service.print(structure_to_print)

    async def action_maintenance_matcher_restore(self, directory):
        """
        Restores the default matchers.
        :param directory: The directory is used to specify the repository.
        :return: None
        """
        matches = self.tack_meta_service.restore_default_matches(directory)

        structure_to_print = {
            'type': 'matcher_restore',
            'root': self.tack_meta_service.get_repository(directory).path,
            'matches': matches
        }

        return self.reporting_service.print(structure_to_print)
