import glob
import os
import importlib.util
import logging
import re

from playhouse.migrate import Database, SchemaMigrator
from cachetools import cached
from cachetools.keys import hashkey
from libs.common.timeit import timeit

from ..models.migration import Migration


@timeit
@cached(cache={}, key=lambda database, migrator, _database_path: hashkey(_database_path))
def migrate_if_needed(database: Database, migrator: SchemaMigrator, _database_path: str):
    """
    Migrates the database when it's needed
    :param database: The database object - already opened
    :param migrator: The migrator object - database specific
    :param _database_path: The path to the database. Dummy parameter for caching
    :return: None
    """
    with database.atomic():
        database.create_tables([Migration])
        all_migration_files = _find_migration_files()
        persisted_migrations = list(Migration.select().order_by(Migration.epoch))

        logging.debug('persisted_migrations: %s', len(persisted_migrations))
        logging.debug('all_migration_files: %s', len(all_migration_files))

        if len(all_migration_files) <= 0:
            raise RuntimeError('Local migration files missing - packaging issue?')

        if len(persisted_migrations) <= 0:
            _execute_migrations(all_migration_files, migrator)
            logging.debug('All migrations were applied (fresh state)')

        elif persisted_migrations[-1].epoch != all_migration_files[-1]['epoch']:
            needed_migration_files = filter(
                lambda migration_file: migration_file['epoch'] > persisted_migrations[-1].epoch, all_migration_files
            )
            _execute_migrations(needed_migration_files, migrator)
            logging.debug('Partial migrations were applied (old state)')

        else:
            logging.debug('Migrations were not applied (latest state)')


def _execute_migrations(migration_files, migrator):
    """
    Executes migrations from migration files
    :param migration_files: The list of files to execute
    :param migrator: The migrator to handle the migration
    :return: None
    """
    for migration_file in migration_files:
        loaded_migration = _load_absolute_module(migration_file['filename'])
        logging.debug('Executing migration %s', migration_file['filename'])
        loaded_migration.migrate_up(migrator)
        Migration.create(epoch=migration_file['epoch'], title=os.path.basename(migration_file['filename']))


def _load_absolute_module(path_to_module):
    """
    Loads python files on runtime and make them available
    :param path_to_module: The path to the python file
    :return: The module we'some_dict like to execute
    """
    spec = importlib.util.spec_from_file_location('i_dont_care',
                                                  path_to_module)
    wanted_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wanted_module)
    return wanted_module


def _find_migration_files():
    """
    Finds migration files in the current directory
    :return: A list of migration files
    """
    folder = os.path.dirname(__file__)
    glob_to_search = f'{folder}/files/migration_*.py'
    files_with_timestamp = []
    for file in glob.glob(glob_to_search):
        logging.debug('Found a file %s', file)
        match = re.search(r'migration_(\d+)_.+.py', file)
        epoch = int(match.group(1))
        files_with_timestamp.append({
            'filename': file,
            'epoch': epoch
        })

    sorted_files_with_timestamp = sorted(files_with_timestamp, key=lambda i: i['epoch'])
    return sorted_files_with_timestamp
