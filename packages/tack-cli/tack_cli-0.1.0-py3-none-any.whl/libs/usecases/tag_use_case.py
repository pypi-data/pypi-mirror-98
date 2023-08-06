import logging
import aiofiles
import aiofiles.os

from libs.storage.service import Service as StorageService
from libs.common.tag_data import TagData
from libs.common.timeit import timeit


class TagUseCase:
    """Use case to manage tags and files"""

    def __init__(self, storage_service: StorageService, tack_meta_service, reporting_service):
        self.storage_service = storage_service
        self.tack_meta_service = tack_meta_service
        self.reporting_service = reporting_service

    @timeit
    async def action_add_tags(self, directory, tag_names, tag_type):
        """
        Adds new tags to the repository.
        :param directory: The location where you want to create a new repository.
        :param tags: The tags to be added
        :param tag_type: The types of tags to be added
        :return: None
        """
        tags = list(map(lambda tag: TagData(tag, tag_type), tag_names))
        handled_tags = await self.storage_service.add_tags(directory, tags)

        structure_to_print = {
            'type': 'add_tags',
            'root': self.tack_meta_service.get_repository(directory).path,
            'handled_tags': list(map(lambda handled_tag: handled_tag.to_dict(), handled_tags)),
        }

        await self.tack_meta_service.calculate_and_write_database_integrity(directory)
        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_delete_tags(self, directory, opts):
        """
        Deletes tags of the repository
        :param directory: The location where you want to create a new repository.
        :param opts: Options that either keep tags or a tagList as parameter
        :return: None
        """

        if opts['tags']:
            tags = opts['tags']
        else:
            async with aiofiles.open(opts['tags_list'], mode='r', encoding='utf-8') as tags_file:
                raw_tags = await tags_file.readlines()
                tags = list(map(lambda raw_tag: raw_tag.strip(), raw_tags))

        deleted_tags = await self.storage_service.delete_tags(directory, tags)

        structure_to_print = {
            'type': 'delete_tags',
            'root': self.tack_meta_service.get_repository(directory).path,
            'deleted_tags': list(map(lambda deleted_tag: deleted_tag.to_dict(), deleted_tags))
        }

        await self.tack_meta_service.calculate_and_write_database_integrity(directory)
        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_find_untagged(self, directory, file_match):
        """
        Finds all files that are not associated to any tags.
        :param directory: The location where you want to create a new repository.
        :param file_match: The file match you want to specify your search on
        :return: None
        """
        untagged_files = await self.storage_service.find_untagged(directory, file_match)

        structure_to_print = {
            'type': 'find_untagged',
            'root': self.tack_meta_service.get_repository(directory).path,
            'untagged_files': untagged_files
        }

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_find_tagged_files(self, directory, tags=None):
        """
        Finds all files that are associated to tags
        :param directory: The location where you want to create a new repository.
        :param tags: The tags you want to specify your search to
        :return: None
        """
        if tags is None:
            tags = []
        tagged_files = await self.storage_service.find_by_tag_combination(directory, tags)
        structure_to_print = {
            'type': 'find_tagged_files',
            'root': self.tack_meta_service.get_repository(directory).path,
            'tags': tags,
            'tagged_files': tagged_files,
        }

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_find_files_with_tag(self, directory, file_match=None):
        """
        Finds any files with tag information.
        :param directory: The location where you want to create a new repository.
        :param file_match: The file match used to specify your search.
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)
        files_with_tags = await self.storage_service.find_by_files(directory, file_match)
        structure_to_print = {
            'type': 'find_files_with_tag',
            'root': repo.path,
            'files_with_tags': files_with_tags
        }

        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_find_tags(self, directory, with_files, in_here, tags):
        """
        Finds any tags in the repository.
        :param directory: The location where you want to create a new repository.
        :param with_files: Also returns the files.
        :param in_here: Searches from the current location only.
        :param tags: Specify the tags you want to look for.
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)

        structure_to_print = {
            'type': 'find_tags',
            'root': repo.path,
            'show_files': with_files
        }

        if in_here:
            logging.debug('using --here flag')
            found_tags = await self.storage_service.get_tags_with_count(directory, tags, in_here, with_files)
        else:
            found_tags = await self.storage_service.get_tags_with_count(repo.path, tags, in_here, with_files)

        structure_to_print['tags'] = dict(sorted(found_tags.items()))
        self.reporting_service.print(structure_to_print)

    @timeit
    async def action_rename_tag(self, directory, tag, new_name):
        """
        Renames a tags to a new name.
        :param directory: The location where you want to create a new repository.
        :param tag: The old tag name.
        :param new_name: The new tag name.
        :return: None
        """
        renamed_tag = await self.storage_service.rename_tag(directory, tag, new_name)

        structure_to_print = {
            'type': 'rename_tag',
            'root': self.tack_meta_service.get_repository(directory).path,
            'renamed_tag': renamed_tag,
        }

        await self.tack_meta_service.calculate_and_write_database_integrity(directory)
        return self.reporting_service.print(structure_to_print)

    @timeit
    async def action_tag_files(self, directory, options):
        """
        Tags files.
        :param directory: The location where you want to create a new repository.
        :param tags: The tags you want to associate to the file match.
        :param file_match: The file match which is used to specify the files.
        :return: None
        """

        repo = self.tack_meta_service.get_repository(directory)
        if options['tags']:
            tags = options['tags']
        else:
            async with aiofiles.open(options['tags_list'], mode='r', encoding='utf-8') as file:
                raw_tags = await file.readlines()
                tags = list(map(lambda raw_tag: raw_tag.strip(), raw_tags))

        if options['file_match']:
            stored_files = await self.storage_service.get_file_list(repo.path, options['file_match'])
        elif options['file_list']:
            async with aiofiles.open(options['file_list'], mode='r', encoding='utf-8') as file:
                proposals = await file.readlines()
            stored_files = await self.storage_service.get_files_by_list(repo.path, proposals)
        else:
            raise BaseException('FML')

        stored_tags = await self.storage_service.get_tags(repo.path, tags)

        logging.debug('Found {%s} tags', len(stored_tags))
        for stored_tag in stored_tags:
            logging.debug('Tag: %s', stored_tag.name)

        logging.debug('Found {%s} files', len(stored_files))
        for stored_file in stored_files:
            logging.debug('File: %s', stored_file)

        data = await self.storage_service.associate_tags_with_files(directory, stored_files, stored_tags)

        structure_to_print = {
            'type': 'tag_files',
            'root': repo.path,
            'data': data
        }

        await self.tack_meta_service.calculate_and_write_database_integrity(directory)
        return self.reporting_service.print(structure_to_print)

    async def action_untag_files(self, directory, options):
        """
        Untags files with tags.
        :param directory: The location where you want to create a new repository.
        :param tags: The tags you want to remove from the file match.
        :param file_match: The specified file match.
        :return: None
        """

        tags = options['tags']
        repo = self.tack_meta_service.get_repository(directory)
        if options['file_match']:
            stored_files = await self.storage_service.get_file_list(repo.path, options['file_match'])
        elif options['file_list']:
            async with aiofiles.open(options['file_list'], mode='r', encoding='utf-8') as file:
                proposals = await file.readlines()
            stored_files = await self.storage_service.get_files_by_list(repo.path, proposals)
        else:
            raise BaseException('FML')

        repo = self.tack_meta_service.get_repository(directory)
        stored_tags = await self.storage_service.get_tags(repo.path, tags)

        logging.debug('Found %s tags', len(stored_tags))
        for stored_tag in stored_tags:
            logging.debug('Tag: %s', stored_tag.name)

        logging.debug('Found %s files', len(stored_files))
        for stored_file in stored_files:
            logging.debug('File: %s', stored_file)

        tag_names = [tag.name for tag in stored_tags]

        data = await self.storage_service.disassociate_tags_with_files(directory, stored_files, tag_names)

        structure_to_print = {
            'type': 'untag_files',
            'root': repo.path,
            'data': data
        }

        await self.tack_meta_service.calculate_and_write_database_integrity(directory)
        return self.reporting_service.print(structure_to_print)
