from libs.common.string_to_bool import string_to_bool


class TackMetaService:
    """
    Service class for tack meta things
    """

    def __init__(self, repository):
        self.repository = repository

    def create_or_read_defaults(self, level, config=None):
        """
        Creates or reads the config at a given location
        :param level: The level to write the config to.
        :param config: The config to create if it can't be read
        :return:
        """
        return self.repository.create_or_read_defaults(level, config)

    def create_defaults(self, level, config=None):
        """
        Creates a config or modifies the existing one
        :param level: The level to write the config to.
        :param config: Return the created config
        :return:
        """
        return self.repository.create_defaults(level, config)

    @staticmethod
    def _set_nested_dict(some_dict, key_list, target_value):
        value = some_dict
        for key in key_list:
            if key not in value:
                value[key] = None
            if isinstance(value[key], dict):
                value = value[key]
            else:
                if target_value is None:
                    del value[key]
                else:
                    value[key] = target_value

    def set_setting(self, directory, opts):
        """
        Sets a setting
        :param directory: Any sub path in the repository.
        :param opts: The key/value you'some_dict like to set as setting.
        :return: Returns the written config.
        """
        repo = self.get_repository(directory)
        key = opts['key']
        # Doing some try parse stuff
        # Bool > Int > Str
        try:
            value = string_to_bool(opts['value'])
        except TypeError:
            try:
                value = int(opts['value'])
            except ValueError:
                value = opts['value']
        self._set_nested_dict(repo.config['settings'], key.split('.'), value)
        return self.repository.write_settings(repo)

    def unset_setting(self, directory, opts):
        """
        Deletes a previously set setting in the repository
        :param directory: Any sub path in the repository.
        :param opts: The options containing the key to unset.
        :return: Returns the written config.
        """
        repo = self.get_repository(directory)
        key = opts['key']
        self._set_nested_dict(repo.config['settings'], key.split('.'), None)
        return self.repository.write_settings(repo)

    def get_settings(self, directory):
        """
        Returns the settings in the repository.
        :param directory: Any sub path in the repository.
        :return: Returns the settings found in the repository.
        """
        repo = self.get_repository(directory)
        return repo.config['settings']

    def get_plugins(self, directory):
        """
        Returns all plugins in the repository.
        :param directory: Any sub path in the repository.
        :return: A list of plugins
        """
        repo = self.get_repository(directory)
        return repo.config['settings']['plugins']

    def create_repository(self, directory):
        """
        Creates a new repository in the specified path.
        :param directory: Any sub path in the repository.
        :return: (create, path)
        """
        return self.repository.create_repository(directory)

    def calculate_integrity(self, directory):
        """
        Calculates the integrity of the repository.
        :param directory: Any sub path in the repository.
        :return: Returns the hash of the repository.
        """
        return self.repository.calculate_integrity(directory)

    def write_integrity(self, directory, integrity):
        """
        Writes the integrity to the repository.
        :param directory: Any sub path in the repository.
        :param integrity: The calculated integrity.
        :return: None
        """
        return self.repository.write_integrity(directory, integrity)

    def calculate_and_write_database_integrity(self, directory):
        """
        Calculates and writes the integrity of the repository.
        :param directory: Any sub path in the repository.
        :return: None
        """
        return self.repository.calculate_and_write_database_integrity(directory)

    def get_repository(self, directory):
        """
       Returns the config of the repository.
       :param directory: Any sub path in the repository.
       :return: The config of the repository.
       """
        return self.repository.get_repository(directory)

    def find_repository(self, directory):
        """
        Attempts to find the repository in any path and stops once the top-path is reached.
        :param directory: Any sub path in the repository.
        :return: Returns the path of the found repository.
        """
        return self.repository.find_repository(directory)

    def get_ignored_matches(self, directory):
        """
        Reads the config and returns the matches.
        :param directory: Any sub path in the repository.
        :return: The found matches
        """
        return self.repository.get_ignored_matches(directory)

    def add_to_ignored_matches(self, directory, match_to_ignore):
        """
        Adds a match to the repository.
        :param directory: Any sub path in the repository.
        :param match_to_ignore: The match to be added.
        :return: Returns a boolean if the match was written.
        """
        return self.repository.add_to_ignored_matches(directory, match_to_ignore)

    def delete_from_ignored_matches(self, directory, match_to_remove):
        """
        Deletes a match from the repository.
        :param directory: Any sub path in the repository.
        :param match_to_remove: The match that is to be removed.
        :return: Returns the item and the index from the removed match.
        """
        return self.repository.delete_from_ignored_matches(directory, match_to_remove)

    def restore_default_matches(self, directory):
        """
        Restores the default matchers.
        :param directory: Any sub path in the repository.
        :return: Returns the default matchers.
        """
        return self.repository.restore_default_matches(directory)
