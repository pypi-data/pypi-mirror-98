from operator import itemgetter
import logging

import libs.common.timeit as timeit
from libs.common.file_data import FileData


# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
class Suggest:
    """Use case to suggest tags for files"""

    def __init__(self, storage_service, tag_operations, tag_suggestion, reporting_service, tack_meta_service):
        self.storage_service = storage_service
        self.tag_operations = tag_operations
        self.tag_suggestion = tag_suggestion
        self.reporting_service = reporting_service
        self.tack_meta_service = tack_meta_service

    @timeit.timeit
    async def suggest_tag(self, directory, file_match, apply=False, _detailed=False):  # pylint: disable-msg=too-many-locals
        """
        Suggests a tag for the specified file match
        :param directory: The directory is used to specify the repository.
        :param file_match: The file match which is used to find the files
        :param apply: Applies the suggested tags directly
        :param _detailed: NOP
        :return: None
        """
        repo = self.tack_meta_service.get_repository(directory)
        indexed_files = await self.storage_service.find_untagged(repo.path, file_match)
        existing_tags = await self.storage_service.get_tags(repo.path)

        structure_to_print = {
            'type': 'suggest',
            'root': repo.path,
            'applied': False,
            'untagged_files': sorted(list(indexed_files)),
            'files': []
        }

        existing_tag_names = {existing_tag.name for existing_tag in existing_tags}
        suggested_tags = set()
        indexed_files_with_suggestions = []
        all_file_tags = []
        for file in indexed_files:
            tag_suggestions = self.tag_suggestion.suggest_tag(repo.path, file)
            if len(tag_suggestions) <= 0:
                logging.warning('"%s" has no tag suggestions', file)
                continue

            file_tags = {
                'path': file,
                'tags': [tag_suggestion.to_dict() for tag_suggestion in tag_suggestions]
            }
            all_file_tags.append(file_tags)

            file_with_suggestion = FileData(path=file, suggested_tags=tag_suggestions)
            indexed_files_with_suggestions.append(file_with_suggestion)
            suggested_tags.update(tag_suggestions)

        structure_to_print['files'] = sorted(all_file_tags, key=itemgetter('path'))
        unknown_tags = suggested_tags - existing_tag_names
        structure_to_print['unknown_tags'] = sorted(list([unknown_tag.to_dict() for unknown_tag in unknown_tags]),
                                                    key=lambda x: x['name'])

        if apply:
            structure_to_print['applied'] = True
            await self.storage_service.add_tags(directory, unknown_tags)

            await self._separated_insert(directory, indexed_files_with_suggestions)

        await self.tack_meta_service.calculate_and_write_database_integrity(directory)
        self.reporting_service.print(structure_to_print)

    async def _separated_insert(self, directory, indexed_files_with_suggestions):
        compound_tags = {}
        for file in indexed_files_with_suggestions:
            compound = "|".join([str(xxx) for xxx in file.suggested_tags])
            xxx = compound_tags.get(compound, {'tags': file.suggested_tags, 'files': []})
            xxx['files'].append(file)
            compound_tags[compound] = xxx

        for _compound, xxx in compound_tags.items():
            await self.storage_service.associate_tags_with_files(directory, xxx['files'], xxx['tags'])
