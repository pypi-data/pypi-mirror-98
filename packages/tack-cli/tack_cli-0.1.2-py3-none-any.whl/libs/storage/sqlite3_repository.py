import os
import logging
from typing import List

from peewee import fn, IntegrityError, DoesNotExist, SqliteDatabase, JOIN
from playhouse import shortcuts
from playhouse.migrate import SqliteMigrator

import libs.constants as constants
from libs.common.tag_data import TagData
from libs.common.file_data import FileData
from libs.common.array_extensions import chunk
from .models.tag_type import TagType
from .models.file import File
from .models.tag import Tag
from .models.tagged_file import TaggedFile
from .models.migration import Migration
from .migrations.run_migrations_if_needed import migrate_if_needed
from ..common.timeit import timeit

peewee_logger = logging.getLogger('peewee')
peewee_logger.setLevel(logging.CRITICAL)


class Sqlite3Repository:
    """The class that handles everything the sqlite database."""

    def __init__(self, tack_meta_service):
        self.tack_meta_service = tack_meta_service

    async def add_tags(self, directory: str, tags: List[TagData]) -> List[TagData]:
        """
        Adds tags to the database.
        :param directory: Any sub path in the repository.
        :param tags: The tags to add to the database.
        :return: Returns a list of handled tags.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        handled_tags: List[TagData] = []
        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                for tag in tags:
                    tag_type = tag.type
                    if tag_type is None:
                        tag_type = 'custom'

                    (tag_type_in_database, _exists) = TagType.get_or_create(name=tag_type)
                    logging.debug('Tag type id in database is "%s" for type "%s"', tag_type_in_database, tag_type)
                    handled_tag = TagData(tag.name, tag_type_in_database.name, tag.origin, True)
                    try:
                        tag_in_db = Tag(name=tag.name, type=tag_type_in_database)
                        tag_in_db.save()
                    except IntegrityError as exc:
                        logging.debug('Had an integrity error but consider it duplicate record: "%s"', exc)
                        handled_tag.operation_succeeded = False
                        db.rollback()
                    finally:
                        handled_tags.append(handled_tag)

            return handled_tags

    async def find_by_tag(self, directory, search_tag):
        """
        Finds files in the database based on the tag.
        :param directory: Any sub path in the repository.
        :param search_tag: The tag to identify the file.
        :return: A list of files.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                return [FileData(path=file.path) for file in
                        File.select().join(TaggedFile).join(Tag).where(Tag.name.contains(search_tag))]

    async def find_by_tag_combination(self, directory, tags):
        """
        Finds files based on different tag combinations.
        :param directory: Any sub path in the repository.
        :param tags: The tags that all need to apply to the file.
        :return: A list of files
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                query = File.select().join(TaggedFile).join(Tag).group_by(File.path)
                for tag in tags:
                    query = query.having(fn.max(Tag.name == tag) == 1)

                return [file.path for file in query]

    @timeit
    async def find_by_files(self, directory, file_match):  # pylint: disable-msg=too-many-locals
        """
        Returns a list of files based on input file match.
        :param directory: Any sub path in the repository.
        :param file_match: The file match used to filter down files.
        :return: The list of found files.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)
        with InitializeDatabase(repo) as db:
            with db.atomic():
                result = dict()
                big_query = (File.select(File, Tag.name)
                             .join(TaggedFile, JOIN.LEFT_OUTER)
                             .join(Tag, JOIN.LEFT_OUTER))
                if file_match is not None:
                    big_query = big_query.where(File.path.contains(file_match))

                for file_id, path, modify_time, create_time, size, fingerprint, tag_name in db.execute(big_query):
                    file_entry = FileData(path=path, modify_time=modify_time, create_time=create_time,
                                          size=size, fingerprint=fingerprint).to_dict()
                    tag_entry = TagData(tag_name, None, None).to_dict() if tag_name is not None else None
                    if file_id in result:
                        if 'tags' not in result[file_id]:
                            tags = [tag_entry]
                        else:
                            tags = result[file_id]['tags']
                            tags.append(tag_entry)
                    elif tag_entry is not None:
                        tags = [tag_entry]
                    else:
                        tags = []

                    result[file_id] = {
                        'file': file_entry,
                        'tags': tags
                    }

            return list(result.values())

    async def find_untagged(self, directory, file_match):
        """
        Finds untagged files in the database.
        :param directory: Any sub path in the repository.
        :param file_match: The file match that specifies the files.
        :return: The list of found files.
        """
        logging.debug('Finding untagged files (files with no tag)')
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        if file_match is None:
            file_match = ''

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                subquery = TaggedFile.select(TaggedFile.file).alias('subquery')
                query = File.select().where(File.path.contains(file_match)).where(File.id.not_in(subquery))
                return [file.path for file in query]

    async def delete_tags(self, directory, tags: List[str]) -> List[TagData]:
        """
        Deletes tags in the database.
        :param directory: Any sub path in the repository.
        :param tags: The tags to be delete.
        :return: None
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                find_tags_query = Tag.select().join(TagType)
                delete_tag_query = Tag.delete()

                find_tags_query = find_tags_query.where(Tag.name.in_(tags))
                delete_tag_query = delete_tag_query.where(Tag.name.in_(tags))

                deleted_tags = [
                    TagData(raw.name, raw.type.name, None, True) for
                    raw in
                    find_tags_query.where(TagType.id == Tag.type)
                ]
                TaggedFile.delete().where(TaggedFile.tag.in_(find_tags_query)).execute()
                delete_tag_query.execute()

            return deleted_tags

    async def get_files_by_list(self, directory, file_list):
        """
        Returns a list of files based on the input file list
        :param directory: Any sub path in the repository.
        :param file_list: The list of files to look for
        :return: Returns the actual file list
        """
        repo = self.tack_meta_service.get_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo.path)
        with initialize_database:
            cleaned_file_list = list(map(lambda file: file.replace(repo.path + os.path.sep, '')
                                         .replace('\\', '/').strip(), file_list))
            sql = File.select().where(File.path << cleaned_file_list)
            logging.debug('SQL: %s', sql)
            return [FileData(
                path=raw_file.path,
                modify_time=raw_file.modify_time,
                create_time=raw_file.create_time,
                size=raw_file.size,
                fingerprint=raw_file.fingerprint,
                suggested_tags='',
            ) for raw_file in sql]

    async def get_file_list(self, directory, file_match):
        """
        Returns a list of all files.
        :param directory: Any sub path in the repository.
        :param file_match: The file match to specify files.
        :return: The list of files.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database:
            return [FileData(
                path=raw_file.path,
                modify_time=raw_file.modify_time,
                create_time=raw_file.create_time,
                size=raw_file.size,
                fingerprint=raw_file.fingerprint,
                suggested_tags='',
            ) for raw_file in File.select().where(File.path.contains(file_match))]

    async def add_files(self, directory, added_files):
        """
        Saves newly added files to the database.
        :param directory: Any sub path in the repository.
        :param added_files: The added files.
        :return: None
        """
        if len(added_files) <= 0:
            return

        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)
        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                for file in added_files:
                    file_in_db = File(path=file.path,
                                      fingerprint=file.fingerprint,
                                      modify_time=file.modify_time,
                                      create_time=file.create_time,
                                      size=file.size)
                    file_in_db.save()

    async def remove_files(self, directory, removed_files):
        """
        Removes files from the index.
        :param directory: Any sub path in the repository.
        :param removed_files: The removed files
        :return: None
        """
        if len(removed_files) <= 0:
            return

        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                for file in removed_files:
                    File.delete().where(File.path == file.path).execute()

    async def rename_files(self, directory, renamed_files):
        """
        Renames the files in the database
        :param directory: Any sub path in the repository.
        :param renamed_files: The renamed files
        :return: None
        """
        if len(renamed_files) <= 0:
            return

        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                for file in renamed_files.values():
                    File.update({
                        File.path: file.new_path,
                        File.create_time: file.new_create_time
                    }).where(File.path == file.path).execute()

    async def modify_files(self, directory, modified_files):
        """
        Modifies the files in the database.
        :param directory: Any sub path in the repository.
        :param modified_files: The modified files.
        :return: None
        """
        if len(modified_files) <= 0:
            return

        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                for file in modified_files:
                    File.update({
                        File.size: file.size,
                        File.create_time: file.create_time,
                        File.modify_time: file.modify_time,
                        File.fingerprint: file.fingerprint
                    }).where(File.path == file.path).execute()

    async def get_tags(self, directory, tags) -> List[TagData]:
        """
        Returns tags in the database.
        :param directory: Any sub path in the repository.
        :param tags: The tags you want to find, can be empty.
        :return: The list of found tags.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                query = Tag.select(Tag.name).join(TagType).where(Tag.name.in_(tags))

                return [TagData(tag.name, tag.type, None) for tag in query]

    async def get_tags_with_count(self, directory, tags, is_relative, with_files):  # pylint: disable-msg=too-many-locals
        """
        Returns tags with associated files.
        :param with_files: Specifies if you'd like to include files in the tags.
        :param directory: Any sub path in the repository.
        :param tags: The tags you want to find.
        :param is_relative: A relative location in the filesystem to match by.
        :return: A list of tags with associated files.
        """
        logging.debug('directory: %s', directory)

        repo = self.tack_meta_service.find_repository(directory)
        repo = repo.replace('\\', '/')
        await self._create_tables_if_needed(directory)

        relative_path = os.path.abspath(directory).replace('\\', '/').replace(repo + '/', '')
        logging.debug('relative_path: %s', relative_path)

        with InitializeDatabase(repo) as db:
            with db.atomic():
                if with_files is False:
                    query = (Tag.select(Tag, fn.Count(TaggedFile.file).alias('count'))
                             .join(TaggedFile, JOIN.LEFT_OUTER)
                             .join(File, JOIN.LEFT_OUTER))
                    if len(tags) > 0:
                        query = query.where(Tag.name.in_(tags))

                    if is_relative:
                        query = query.where(File.path.contains(relative_path))

                    query = query.group_by(Tag)
                    tags_with_counts = query.execute()

                    result = dict()
                    for tag_with_counts in tags_with_counts:
                        result[tag_with_counts.name] = [''] * tag_with_counts.count

                    return result

                # Less efficient stuff - to be crying about :(
                tag_query = Tag.select()

                for tag in tags:
                    tag_query = tag_query.where(Tag.name.contains(tag)).order_by(Tag.name)

                result = dict()
                for tag in tag_query.execute():
                    if with_files:
                        files_query = File.select(File.path).join(TaggedFile).where(TaggedFile.tag == tag.id)
                        if is_relative:
                            files_query = files_query.where(File.path.contains(relative_path))

                        file_paths = [file.path for file in files_query]
                    else:
                        quick_query = File.select().join(TaggedFile).where(TaggedFile.tag == tag.id)
                        if is_relative:
                            quick_query = quick_query.where(File.path.contains(relative_path))
                        count = quick_query.count()
                        file_paths = [] * count
                    result[tag.name] = file_paths

                return result

    async def associate_tags_with_files(self, directory, files, tags: List[TagData]):  # pylint: disable-msg=too-many-locals
        """
        Associates files with tags.
        :param directory: Any sub path in the repository.
        :param files: The files you want to associate.
        :param tags: All the tags to be associated with the files.
        :return: Returns the list of associated files & tags.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        with InitializeDatabase(repo) as db:
            file_paths = list(map(lambda x: x.path, files))
            tag_types = list(filter(lambda x: x, map(lambda x: x.type, tags)))
            tag_names = list(map(lambda x: x.name, tags))
            with db.atomic():
                db_tag_types = TagType.select()
                if len(tag_types) > 0:
                    db_tag_types.where(TagType.id << tag_types)
                db_files = File.select().where(File.path << file_paths)
                db_tags = Tag.select().where(Tag.name << tag_names).where(Tag.type << db_tag_types)

            data = []
            for db_file in db_files:
                for db_tag in db_tags:
                    data.append((db_file, db_tag))

            # sqlite has a limit of 999 concurrent inserts
            # ref: https://github.com/coleifer/peewee/issues/1641
            for batch in chunk(data, 499):
                with db.atomic():
                    try:
                        TaggedFile.insert_many(batch, fields=[TaggedFile.file, TaggedFile.tag]).execute(db)
                    except IntegrityError as exc:
                        msg = str(exc)
                        if 'UNIQUE' in msg:
                            logging.debug('File was already associated with the tag.')
                            logging.debug(exc)
                        else:
                            raise exc

            return [
                {
                    'file': shortcuts.model_to_dict(file),
                    'tag': TagData(tag.name, tag.type.name, None, True).to_dict()
                }
                for (file, tag) in data
            ]

    async def disassociate_tags_with_files(self, directory, files, tag_names):
        """
        Disassociates the tags and files
        :param directory: Any sub path in the repository.
        :param files: The files you want to disassociate.
        :param tag_names: The tags you want to disassociate the files from.
        :return: Returns the list of files and tags you disassociated.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            data = []
            file_paths = list(map(lambda x: x.path, files))
            with db.atomic():
                db_files = File.select().where(File.path << file_paths)
                db_tags = Tag.select().where(Tag.name << tag_names)

                for db_file in db_files:
                    for db_tag in db_tags:
                        deleted_rows = TaggedFile.delete().where(TaggedFile.tag == db_tag, TaggedFile.file == db_file) \
                            .execute()
                        if deleted_rows > 0:
                            data.append({
                                'file': shortcuts.model_to_dict(db_file),
                                'tag': TagData(db_tag.name, db_tag.type.name).to_dict()
                            })

            return data

    async def stats(self, directory):
        """
        Returns stats for the database
        :param directory:  Any sub path in the repository.
        :return: The stats from the database.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            structure = {}

            with db.atomic():
                structure['tag_count'] = Tag.select().count(database=db)
                structure['file_count'] = File.select().count(database=db)
                structure['associations'] = TaggedFile.select().count(database=db)

            return structure

    async def rename_tag(self, directory, tag, new_name):
        """
        Renames a tag.
        :param directory: Any sub path in the repository.
        :param tag: The old tag name
        :param new_name: The new tag name
        :return: Returns the renamed tag.
        """
        repo = self.tack_meta_service.find_repository(directory)
        await self._create_tables_if_needed(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            result = {
                'old_name': tag,
                'new_name': tag,
                'renamed': False
            }
            with db.atomic():
                try:
                    Tag.get(Tag.name == tag)
                except DoesNotExist:
                    result['reason'] = 'Tag not found'
                    result['code'] = 1
                    return result

                try:
                    updated_rows = Tag.update(name=new_name).where(Tag.name == tag).execute()

                    if updated_rows > 0:
                        result['new_name'] = new_name
                        result['renamed'] = True
                except IntegrityError as exc:
                    msg = str(exc)
                    if 'UNIQUE' in msg:
                        result['reason'] = 'New tag name already taken'
                        result['code'] = 2
            return result

    async def _create_tables_if_needed(self, directory):
        repo = self.tack_meta_service.find_repository(directory)

        path_to_database = os.path.join(repo, constants.repository_storage)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            await migrate_if_needed(db, SqliteMigrator(db), path_to_database)

    def _create_all_tables(self, directory):
        repo = self.tack_meta_service.find_repository(directory)

        initialize_database = InitializeDatabase(repo)
        with initialize_database as db:
            with db.atomic():
                db.create_tables([Tag, File, TaggedFile, TagType])


class InitializeDatabase:
    """
    Initializes the database and closes the connection if the scope is left.
    """

    def __init__(self, repo):
        self._db = None
        self._repo = repo

    def __enter__(self):
        self._db = SqliteDatabase(os.path.join(self._repo, constants.repository_storage), pragmas=(
            ('threadlocals', True),
            ('journal_mode', 'wal')
        ))
        self._db.bind([Tag, File, TaggedFile, Migration, TagType])
        return self._db

    def __exit__(self, _type, _value, _traceback):
        self._db.close()
