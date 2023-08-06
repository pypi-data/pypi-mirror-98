import re

from libs.common.tag_data import TagData


class Service:
    """
    Service class for suggestions
    """
    def __init__(self, repositories, metadata_service, *plugins):
        self.repositories = repositories
        self.metadata_service = metadata_service
        self.plugins = plugins

    def suggest_tag(self, path_of_repo, file):
        """
        Suggest tags for the specified file
        :param path_of_repo: The path of the repo.
        :param file: The file to apply the rule to.
        :return: Returns a list of tags used as suggestion.
        """
        suggested_tags = []
        for repository in self.repositories:
            if re.match(repository.compatible_files, file):
                suggested_tags += repository.suggest_tag(path_of_repo, file)

        current_plugins = self.metadata_service.get_plugins(path_of_repo)
        for plugin in self.plugins:
            plugin_config = current_plugins[type(plugin).__name__]
            if plugin_config['enabled']:
                raw_plugin_tags = plugin.process(path_of_repo=path_of_repo, file=file)
                plugin_tags = [TagData(tag['tag'], tag['type'], type(plugin).__name__) for tag in raw_plugin_tags]
                suggested_tags += plugin_tags

        return suggested_tags
