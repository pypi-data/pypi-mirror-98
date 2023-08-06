import os

from mp3_tagger import MP3File

from libs.common.tag_data import TagData


class SuggestMp3Repository:
    """The file path repository creates suggestions for the files."""
    def __init__(self):
        pass

    @property
    def compatible_files(self):
        """compatible_files"""
        return ".*mp3$"

    @staticmethod
    def suggest_tag(path_of_repo, file):
        """
        Suggest tags for the specified file
        :param path_of_repo: Path of the repository
        :param file: The files to apply the rule to.
        :return: Returns a list of tags used as suggestion.
        """

        mp3 = MP3File(os.path.join(path_of_repo, file))
        tags = set()
        for _key, available_tags in mp3.get_tags().items():
            for tag_type, tag_value in available_tags.items():
                if tag_value:
                    if tag_type in ['artist', 'album']:
                        tag = TagData(str(tag_value), tag_type, 'mp3')
                        tags.add(tag)

        return tags
