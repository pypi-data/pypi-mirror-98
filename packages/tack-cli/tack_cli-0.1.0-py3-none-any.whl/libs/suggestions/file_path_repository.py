import os

from libs.common.tag_data import TagData


class FilePathRepository:
    """The file path repository creates suggestions for the files."""
    def __init__(self):
        pass

    @property
    def compatible_files(self):
        """compatible_files"""
        return ".*"

    def suggest_tag(self, _path_of_repo, file):
        """
        Suggest tags for the specified file
        :param _path_of_repo: NOP
        :param file: The files to apply the rule to.
        :return: Returns a list of tags used as suggestion.
        """
        path_segments = os.path.dirname(file).split('/')

        if len(path_segments) == 1 and path_segments[0] == '':
            return []

        cleaned_tags = []
        for suggested_tag in path_segments:
            proposal = self._clean_tag_name(suggested_tag)
            if proposal is None:
                continue

            if len(proposal) <= 0:
                continue

            cleaned_tags.append(TagData(proposal, 'file_path', 'file_path'))

        return cleaned_tags

    def _clean_tag_name(self, tag):
        tag = self._replace_underscore_with_space(tag)
        return tag.strip()

    @staticmethod
    def _replace_underscore_with_space(tag):
        if '_' not in tag:
            return tag

        elements = tag.split('_')
        capitalized = list(map(lambda x: x.capitalize(), elements))
        return ' '.join(capitalized)
