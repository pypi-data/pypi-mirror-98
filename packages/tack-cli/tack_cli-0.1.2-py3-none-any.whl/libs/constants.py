import os
from pathlib import Path

REPOSITORY_DIRECTORY_NAME = '.tack'
repository_metadata_file_name = os.path.join(REPOSITORY_DIRECTORY_NAME, 'metadata.toml')
repository_storage = os.path.join(REPOSITORY_DIRECTORY_NAME, 'storage.db')

files_directory_folder = os.path.join(REPOSITORY_DIRECTORY_NAME, 'files')
files_raw_file_name = os.path.join(files_directory_folder, 'raw.toml')
files_tag_file_name = os.path.join(files_directory_folder, 'tag.toml')

tags_directory_folder = os.path.join(REPOSITORY_DIRECTORY_NAME, 'tags')

TMP_SUFFIX = '.tmp'

ignored_matches = sorted([
    '\\.tack',
    '/.tack',
    '\\.git',
    '/.git',
])

plugins_folders = [
    os.path.join(os.path.dirname(__file__), '..', 'plugins'),
    os.path.join(Path.home(), '.tack', 'plugins')
]

CONFIG_NAME = 'config.toml'
METADATA_DEFAULTS = 'metadata.defaults.toml'
config_levels = [
    'system',
    'user',
    'repository'
]
