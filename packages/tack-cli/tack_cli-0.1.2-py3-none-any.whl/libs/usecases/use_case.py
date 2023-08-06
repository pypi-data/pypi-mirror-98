import logging

from libs.common.timeit import timeit
from libs.common.file_data import FileData


class UseCase:
    """Generic use-case class to handle unspecified use cases"""

    def __init__(self, storage_service, tag_operations, reporting_service, tack_meta_service):
        self.storage_service = storage_service
        self.tag_operations = tag_operations
        self.reporting_service = reporting_service
        self.tack_meta_service = tack_meta_service

    @timeit
    async def action_refresh(self, directory):
        """
        Refreshes the file index of the repository. Hashes files if needed and compares against the current index.
        :param directory: The directory is used to specify the repository.
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)

        logging.info('Refreshing database in "%s"', repo.path)

        # we use this to change the keys of the thing..
        current_files_without_fingerprint = await self.tag_operations.find_files(
            repo.path,
            repo.config['settings']['ignored_matches']
        )
        indexed_files = await self.storage_service.get_file_list(repo.path)

        FileData.key_args = ['path', 'suggested_tags', 'size', 'modify_time', 'create_time']
        modified_content = set(current_files_without_fingerprint) - set(indexed_files)

        FileData.key_args = ['path']
        added = set(current_files_without_fingerprint) - set(indexed_files)
        removed = set(indexed_files) - set(current_files_without_fingerprint)

        modified_content = set(list(modified_content)) - added

        structure_to_print = {
            'type': 'refresh',
            'root': repo.path,
            'changed': False
        }

        if len(added) == 0 and len(removed) == 0 and len(modified_content) == 0:
            pass
        else:
            structure_to_print = await self._build_updated_file_index(directory,
                                                                      repo,
                                                                      modified_content,
                                                                      current_files_without_fingerprint,
                                                                      indexed_files,
                                                                      added,
                                                                      removed,
                                                                      structure_to_print)

        await self.tack_meta_service.calculate_and_write_database_integrity(directory)

        return self.reporting_service.print(structure_to_print)

    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-arguments
    async def _build_updated_file_index(self, directory, repo, modified_content, current_files_without_fingerprint,
                                        indexed_files, added, removed, structure_to_print):
        added_with_fingerprint = await self.tag_operations.fingerprint_files(repo.path, list(added))
        modified_with_fingerprint = await self.tag_operations.fingerprint_files(repo.path, list(modified_content))

        FileData.key_args = ['fingerprint']
        renamed_from = set(list(added_with_fingerprint)) & set(list(removed))
        renamed_to = set(list(removed)) & set(list(added_with_fingerprint))

        renamed_files = dict()
        for previous_file in renamed_from:
            renamed_files[previous_file.fingerprint] = previous_file

        for current_file in renamed_to:
            renamed_files[current_file.fingerprint].new_path = current_file.path
            renamed_files[current_file.fingerprint].new_create_time = current_file.create_time

        FileData.key_args = ['path']
        cleaned_added = set(list(added_with_fingerprint)) - set(list(renamed_to))
        cleaned_removed = set(list(removed)) - set(list(renamed_from))
        cleaned_modified = set(list(modified_with_fingerprint)) - set(list(renamed_to))

        structure_to_print['changed'] = True
        structure_to_print['files_on_fs'] = len(current_files_without_fingerprint)
        structure_to_print['files_on_index'] = len(indexed_files)
        structure_to_print['added_files'] = len(cleaned_added)
        structure_to_print['removed_files'] = len(cleaned_removed)
        structure_to_print['renamed_files'] = len(renamed_files)
        structure_to_print['modified_files'] = len(cleaned_modified)

        await self.storage_service.add_files(directory, cleaned_added)
        await self.storage_service.remove_files(directory, cleaned_removed)
        await self.storage_service.rename_files(directory, renamed_files)
        await self.storage_service.modify_files(directory, modified_with_fingerprint)

        return structure_to_print

    # pylint: enable-msg=too-many-locals
    # pylint: enable-msg=too-many-arguments
    @timeit
    async def action_list_files(self, directory):
        """
        Lists all files in the specified location (not the indexed ones!)
        :param directory: The directory is used to specify the repository.
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)

        file_data_objects = await self.tag_operations.find_files(repo.path, repo.config['ignored_matches'])
        files = list(map(lambda x: x.to_dict(), file_data_objects))

        structure_to_print = {
            'type': 'list_files',
            'root': repo.path,
            'files': files
        }

        return self.reporting_service.print(structure_to_print)
