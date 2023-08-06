import glob
import importlib
import logging
from pathlib import Path
from libs.constants import plugins_folders
from .base_plugin import BasePlugin

logger = logging.getLogger('plugin-loader')


def load_plugins():
    """
    Loads plugins and initializes them.
    :return: Returns a list of plugins.
    """
    found_plugins = find_plugin_modules()
    initialized_plugins = [initialize_plugin(x) for x in found_plugins]
    checked_plugins = [check_plugin_functions(x) for x in initialized_plugins]
    valid_plugins = filter(lambda plugin: plugin is not None, checked_plugins)
    return list(valid_plugins)


def check_plugin_functions(plugin_class):
    """
    Checks if the plugin is fulfilling the API spec of the interface
    :param plugin_class: The parsed plugin class (plugin itself)
    :return: Returns the plugin_class if successful, otherwise None
    """
    if plugin_class is None:
        return None

    try:
        instance: BasePlugin = plugin_class()
        logger.info('Loading plugin "%s" from "%s" to extend "%s"',
                    instance.__class__.__name__,
                    instance.author,
                    instance.extends_repository)
        logger.debug(instance.description)

        if 'process' not in dir(instance):
            logger.info('Plugin "%s" didnt implement the needed function "%s"', instance.__class__.__name__, 'process')
            return None

        return plugin_class
    except AttributeError:
        logger.info('Plugin %s is invalid', plugin_class)
        return None


def initialize_plugin(path_to_module):
    """
    Initializes plugin files by parsing and compiling them.
    :param path_to_module: The path to a module to be parsed.
    :return: Returns the parsed class or None
    """
    try:
        spec = importlib.util.spec_from_file_location('',
                                                      path_to_module)
        wanted_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wanted_module)
        return wanted_module.get_class()
    except AttributeError:
        logger.info('Could not load plugin from %s', path_to_module)
        return None


def find_plugin_modules():
    """
    Attempts to find plugin modules in a folder so they can be considered later.
    :return: A list of paths to python files.
    """

    def _find_modules_in_plugin_folder(plugin_folder: str):
        files_to_search = f'{plugin_folder}/*_plugin.py'
        glob_to_search = f'{plugin_folder}/**/*_plugin.py'
        plugins_files = glob.glob(files_to_search)
        plugins_modules = glob.glob(glob_to_search)

        return list(map(lambda file: str(Path(file).resolve()), plugins_files + plugins_modules))

    meta_maps = map(_find_modules_in_plugin_folder, plugins_folders)
    found_modules = []
    for meta_map in meta_maps:
        found_modules.extend(meta_map)
    return found_modules
