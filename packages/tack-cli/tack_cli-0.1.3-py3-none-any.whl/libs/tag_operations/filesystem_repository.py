from pathlib import PurePath, Path
import os
import logging
import asyncio
import filetype

import aiofiles


from libs.common.file_data import FileData
from libs.common.array_extensions import find, chunk
from libs.common.hashing.sha512 import Sha512


class FilesystemRepository:
    """The filesystem repository is doing everything with file operations."""

    def __init__(self, reporting_service):
        self.reporting_service = reporting_service

    FINGERPRINT_SAMPLE_COUNT = 5
    FINGERPRINT_SAMPLE_SIZE = 1024
    CONCURRENT_OPEN_FILES = 100

    @staticmethod
    def _get_match(matches, some_path):
        return find(matches, lambda ignored_sub_path: ignored_sub_path in some_path)

    async def find_files(self, directory, ignored_matches):
        """
        Finds files in a specified directory.
        :param directory: Any sub path in the repository.
        :param ignored_matches: The ignore rules
        :return: Returns an array with found files.
        """
        found_files = []
        for file in Path(directory).glob('**/*'):
            combined = str(PurePath(file.parent, file.name))
            (found, used_match) = self._get_match(ignored_matches, combined)
            if found:
                logging.info('Ignored the path "%s" based on rule "%s"', combined, used_match)
                continue

            if not file.is_file():
                continue

            stat_object = file.stat()

            file_mtime = stat_object.st_mtime_ns
            file_ctime = stat_object.st_ctime_ns
            relative_path = str(PurePath(str(file.parent).replace(directory, './'), file.name)).replace('\\', '/')

            file_size = stat_object.st_size

            file_fingerprint = ''
            file_data = FileData(id=None,
                                 path=relative_path,
                                 size=file_size,
                                 modify_time=file_mtime,
                                 create_time=file_ctime,
                                 suggested_tags='',
                                 fingerprint=file_fingerprint)
            found_files.append(file_data)

        return found_files

    def _calculate_progress(self, percent_completion):
        reporting_structure = {
            'type': 'progress',
            'progress': percent_completion
        }
        self.reporting_service.print(reporting_structure)

    async def fingerprint_files(self, directory, file_data_objects):
        """
        Finger prints the previously found files.
        :param directory: Any sub path in the repository.
        :param file_data_objects: The file objects to be iterated upon.
        :return: Returns a set with the generated fingerprint.
        """
        found_files = self.__file_data_objects_to_dicts(directory, file_data_objects)
        fingerprint_metadata_chunks = chunk(file_data_objects, self.CONCURRENT_OPEN_FILES)
        logging.debug('Found %s files to scan', len(file_data_objects))
        completed_task_count = 0
        for fingerprint_metadata_chunk in fingerprint_metadata_chunks:
            fingerprint_tasks = []
            for file_data_obj in fingerprint_metadata_chunk:
                fingerprint_tasks.append(asyncio.create_task(
                    self.__fingerprint(os.path.join(directory, file_data_obj.path), file_data_obj.size)))

            logging.debug('Waiting for %s tasks', len(fingerprint_tasks))
            finished_tasks, _pending = await asyncio.wait(fingerprint_tasks, return_when=asyncio.ALL_COMPLETED)
            completed_task_count += len(fingerprint_tasks)
            percent_completion = round(completed_task_count / len(file_data_objects) * 100, 2)
            logging.debug('Completed %s tasks (%s%%)', len(fingerprint_tasks), percent_completion)
            self._calculate_progress(percent_completion)

            for task in finished_tasks:
                (known_file_path, fingerprint) = task.result()
                found_files[known_file_path].fingerprint = fingerprint

        return set(found_files.values())

    @staticmethod
    def __file_data_objects_to_dicts(directory, file_data_objects):
        directly_accessible_files = dict()
        for file_data_object in file_data_objects:
            directly_accessible_files[os.path.join(directory, file_data_object.path)] = file_data_object

        return directly_accessible_files

    async def __fingerprint(self, file_path, file_size):
        async with aiofiles.open(file_path, 'rb') as file:
            mime_buffer = await file.read(2048)
            mime_type = filetype.guess_mime(mime_buffer)
            await file.seek(0)

            if mime_type is not None and mime_type.startswith('text/'):
                fingerprint = await Sha512.hash_file(file_path)
                logging.debug('Fingerprinted whole file [%s] "%s": %s', mime_type, file_path, fingerprint)
                return file_path, fingerprint

            if file_size < self.FINGERPRINT_SAMPLE_COUNT * self.FINGERPRINT_SAMPLE_SIZE:
                file_chunk = await file.read()
                with Sha512() as hash_obj:
                    hash_obj.update(file_chunk)
                    fingerprint = hash_obj.hexdigest()
                logging.debug('Fingerprinted small file [%s] "%s": %s', mime_type, file_path, fingerprint)
                return file_path, fingerprint

            step_size = file_size / self.FINGERPRINT_SAMPLE_COUNT
            with Sha512() as hash_obj:
                for step in range(self.FINGERPRINT_SAMPLE_COUNT):
                    await file.seek(int(step * step_size), 0)
                    file_chunk = await file.read(self.FINGERPRINT_SAMPLE_SIZE)
                    hash_obj.update(file_chunk)
                fingerprint = hash_obj.hexdigest()
            logging.debug('Fingerprinted chunks of file [%s] "%s": %s', mime_type, file_path, fingerprint)
            return file_path, fingerprint
