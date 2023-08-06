import os
import logging
import time
import errno
import functools
from pathlib import Path

import aiofiles
import toml

import libs.constants as constants
from libs.storage.repository_hub import RepositoryHub
from libs.common.hashing.crc32 import Crc32
from libs.exceptions.tack_repository_not_found_error import TackRepositoryNotFoundError
from libs.exceptions.tack_permission_error import TackPermissionError


def _get_path_to_config(level):
    if level == 'user':
        base = Path.home()
    elif level == 'system':
        base = Path.home()
    else:
        raise TypeError(f'Could not find {level} in allowed levels.')

    try:
        os.mkdir(os.path.join(base, constants.REPOSITORY_DIRECTORY_NAME))
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
    return os.path.join(base, constants.REPOSITORY_DIRECTORY_NAME, constants.METADATA_DEFAULTS)


class TomlRepository:
    """The repository that handles toml data"""

    def create_or_read_defaults(self, level, config=None):
        """
        Creates or reads the config at a given location
        :param level: The level to write the config to.
        :param config: The config to create if it can't be read
        :return:
        """
        try:
            return self._read_defaults(level)
        except FileNotFoundError:
            return self.create_defaults(level, config)

    @staticmethod
    def create_defaults(level, config=None):
        """
        Creates a config or modifies the existing one
        :param level: The level to write the config to.
        :param config: Return the created config
        :return:
        """
        if config is None:
            config = {
                'plugins': {}
            }

        with open(_get_path_to_config(level), 'w') as file:
            toml.dump(config, file)

        return config

    @staticmethod
    def _read_defaults(level):
        """
        Reads the existing config from a central or repository location
        :param level: The level to write the config to.
        :return: Returns the config object
        """
        return toml.load(_get_path_to_config(level))

    @staticmethod
    def _create_repository_directory_if_needed(directory):
        """
        Creates the directory to the wanted folder if needed.
        :param directory: Any sub path in the repository.
        :return:
        """
        target_folder = os.path.abspath(os.path.join(directory, constants.REPOSITORY_DIRECTORY_NAME))

        try:
            os.mkdir(target_folder)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                return False, target_folder
            if exc.errno == errno.EACCES:
                raise TackPermissionError(f'No permissions in "{directory}"') from exc

            raise

        return True, target_folder

    async def create_repository(self, directory):
        """
        Creates a new repository in the specified path.
        :param directory: Any sub path in the repository.
        :return: (create, path)
        """
        needed_to_create, target_folder = self._create_repository_directory_if_needed(directory)

        repository_config = {
            'creation': time.time(),
            'storage': 'sqlite3',
            'integrity': {
                'database': 0
            },
            'settings': self._read_defaults('user')
        }

        async with aiofiles.open(os.path.join(directory, constants.repository_metadata_file_name), 'w') as file:
            string_to_print = toml.dumps(repository_config)
            await file.write(string_to_print)

        return needed_to_create, target_folder

    async def calculate_integrity(self, directory):
        """
        Calculates the integrity of the repository.
        :param directory: Any sub path in the repository.
        :return: Returns the hash of the repository.
        """
        repo_hub = self.get_repository(directory)
        database = os.path.join(repo_hub.path, constants.repository_storage)
        logging.debug('Calculating crc for database %s', database)
        try:
            database_hash = await Crc32.hash_file(database)
        except FileNotFoundError as exc:
            raise TackRepositoryNotFoundError('Database not found') from exc

        return {
            'database': database_hash
        }

    def write_integrity(self, directory, integrity):
        """
        Writes the integrity to the repository.
        :param directory: Any sub path in the repository.
        :param integrity: The calculated integrity.
        :return: None
        """
        repo_hub = self.get_repository(directory)

        repository_config = repo_hub.config
        repository_config['integrity'] = integrity
        with open(os.path.join(repo_hub.path, constants.repository_metadata_file_name), 'w') as file:
            toml.dump(repository_config, file)

    async def calculate_and_write_database_integrity(self, directory):
        """
        Calculates and writes the integrity of the repository.
        :param directory: Any sub path in the repository.
        :return: None
        """
        integrity = await self.calculate_integrity(directory)
        logging.debug('Integrity of database: %s', integrity)
        self.write_integrity(directory, integrity)

    def get_repository(self, directory):
        """
        Returns the config of the repository.
        :param directory: Any sub path in the repository.
        :return: The config of the repository.
        """
        repo = self.find_repository(directory)

        repository_config = toml.load(os.path.join(repo, constants.repository_metadata_file_name))
        repository_hub = RepositoryHub(repo, repository_config)
        return repository_hub

    @functools.lru_cache(maxsize=100)
    def find_repository(self, directory):
        """
        Attempts to find the repository in any path and stops once the top-path is reached.
        :param directory: Any sub path in the repository.
        :return: Returns the path of the found repository.
        """
        complete_directory = os.path.abspath(directory)
        if self._repository_exists(complete_directory):
            return complete_directory

        new_directory = os.path.abspath(os.path.join(directory, '..'))

        if directory == new_directory:
            logging.debug('found root. Not going further back the directory.')
            raise TackRepositoryNotFoundError('Reached root of drive, no TACK repository found.')

        logging.debug('new directory: %s', new_directory)
        return self.find_repository(new_directory)

    def get_ignored_matches(self, directory):
        """
        Reads the config and returns the matches.
        :param directory: Any sub path in the repository.
        :return: The found matches
        """
        repository_hub = self.get_repository(directory)

        return sorted(repository_hub.config['settings']['ignored_matches'])

    def add_to_ignored_matches(self, directory, match_to_ignore):
        """
        Adds a match to the repository.
        :param directory: Any sub path in the repository.
        :param match_to_ignore: The match to be added.
        :return: Returns a boolean if the match was written.
        """
        repository_hub = self.get_repository(directory)

        ignored_matches = set(repository_hub.config['settings']['ignored_matches'])
        if match_to_ignore in ignored_matches:
            return False

        unix_path = match_to_ignore
        windows_path = match_to_ignore

        ignored_matches.add(unix_path)
        ignored_matches.add(windows_path)

        repository_hub.config['settings']['ignored_matches'] = sorted(list(ignored_matches))

        with open(os.path.join(directory, constants.repository_metadata_file_name), 'w') as file:
            toml.dump(repository_hub.config, file)

        return True

    def delete_from_ignored_matches(self, directory, match_to_remove):
        """
        Deletes a match from the repository.
        :param directory: Any sub path in the repository.
        :param match_to_remove: The match that is to be removed.
        :return: Returns the item and the index from the removed match.
        """
        repository_hub = self.get_repository(directory)

        matchers = self.get_ignored_matches(directory)

        if match_to_remove not in matchers:
            return False, 'Match not found'

        matchers.remove(match_to_remove)

        repository_hub.config['settings']['ignored_matches'] = matchers

        with open(os.path.join(directory, constants.repository_metadata_file_name), 'w') as file:
            toml.dump(repository_hub.config, file)

        return True, {
            'item': match_to_remove,
        }

    @staticmethod
    def write_settings(repository_hub: RepositoryHub):
        """
        Writes the config from the repository to file.
        :param repository_hub: The data structure that holds the config.
        :return: Returns the config that was written.
        """
        with open(os.path.join(repository_hub.path, constants.repository_metadata_file_name), 'w') as file:
            toml.dump(repository_hub.config, file)

            return repository_hub.config

    def restore_default_matches(self, directory):
        """
        Restores the default matchers.
        :param directory: Any sub path in the repository.
        :return: Returns the default matchers.
        """
        default_settings = self._read_defaults('user')
        repository_hub = self.get_repository(directory)
        repository_hub.config['settings']['ignored_matches'] = default_settings['ignored_matches']
        with open(os.path.join(directory, constants.repository_metadata_file_name), 'w') as file:
            toml.dump(repository_hub.config, file)

        return constants.ignored_matches

    @staticmethod
    def _repository_exists(directory):
        metadata_file = os.path.join(directory, constants.repository_metadata_file_name)
        try:
            file = open(metadata_file)
            file.close()
            return True
        except IOError:
            return False
