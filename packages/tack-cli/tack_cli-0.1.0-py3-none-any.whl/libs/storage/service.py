from typing import List

from libs.common.tag_data import TagData


class Service:
    """
    Service class for Storage.
    """
    def __init__(self, repository):
        self.repository = repository

    def add_tags(self, directory, tags):
        """
        Adds tags to the database.
        :param directory: Any sub path in the repository.
        :param tags: The tags to add to the database.
        :return: Returns a list of handled tags.
        """
        return self.repository.add_tags(directory, tags)

    def find_untagged(self, directory, file_match):
        """
       Finds untagged files in the database.
       :param directory: Any sub path in the repository.
       :param file_match: The file match that specifies the files.
       :return: The list of found files.
       """
        return self.repository.find_untagged(directory, file_match)

    def find_by_tag(self, directory, tag):
        """
        Finds files in the database based on the tag.
        :param directory: Any sub path in the repository.
        :param search_tag: The tag to identify the file.
        :return: A list of files.
        """
        return self.repository.find_by_tag(directory, tag)

    def find_by_tag_combination(self, directory, tags):
        """
        Finds files based on different tag combinations.
        :param directory: Any sub path in the repository.
        :param tags: The tags that all need to apply to the file.
        :return: A list of files
        """
        return self.repository.find_by_tag_combination(directory, tags)

    def find_by_files(self, directory, file_match):
        """
        Returns a list of files based on input file match.
        :param directory: Any sub path in the repository.
        :param file_match: The file match used to filter down files.
        :return: The list of found files.
        """
        return self.repository.find_by_files(directory, file_match)

    def delete_tags(self, directory, tags: List[str]) -> List[TagData]:
        """
        Deletes tags in the database.
        :param directory: Any sub path in the repository.
        :param tags: The tags to be delete.
        :return: None
        """
        return self.repository.delete_tags(directory, tags)

    def get_files_by_list(self, directory, file_list):
        """
        Returns a list of files based on the input file list
        :param directory: Any sub path in the repository.
        :param file_list: The list of files to look for
        :return: Returns the actual file list
        """
        return self.repository.get_files_by_list(directory, file_list)

    def get_file_list(self, directory, file_match=''):
        """
        Returns a list of all files.
        :param directory: Any sub path in the repository.
        :param file_match: The file match to specify files.
        :return: The list of files.
        """
        return self.repository.get_file_list(directory, file_match)

    def get_tags(self, directory, tags=None):
        """
        Returns tags in the database.
        :param directory: Any sub path in the repository.
        :param tags: The tags you want to find, can be empty.
        :return: The list of found tags.
        """
        if tags is None:
            tags = []
        return self.repository.get_tags(directory, tags)

    def get_tags_with_count(self, directory, tags=None, is_relative=True, with_files=False):
        """
        Returns tags with associated files.
        :param directory: Any sub path in the repository.
        :param tags: The tags you want to find.
        :param is_relative: A relative location in the filesystem to match by.
        :return: A list of tags with associated files.
        """
        if tags is None:
            tags = []
        return self.repository.get_tags_with_count(directory, tags, is_relative, with_files)

    def associate_tags_with_files(self, directory, files, tag_names):
        """
        Associates files with tags.
        :param directory: Any sub path in the repository.
        :param files: The files you want to associate.
        :param tag_names: The tag names you want to bind to the files.
        :return: Returns the list of associated files & tags.
        """
        return self.repository.associate_tags_with_files(directory, files, tag_names)

    def disassociate_tags_with_files(self, directory, files, tag_names):
        """
        Disassociates the tags and files
        :param directory: Any sub path in the repository.
        :param files: The files you want to disassociate.
        :param tag_names: The tags you want to disassociate the files from.
        :return: Returns the list of files and tags you disassociated.
        """
        return self.repository.disassociate_tags_with_files(directory, files, tag_names)

    def rename_tag(self, directory, tag, new_name):
        """
        Renames a tag.
        :param directory: Any sub path in the repository.
        :param tag: The old tag name
        :param new_name: The new tag name
        :return: Returns the renamed tag.
        """
        return self.repository.rename_tag(directory, tag, new_name)

    def add_files(self, directory, added_files):
        """
        Saves newly added files to the database.
        :param directory: Any sub path in the repository.
        :param added_files: The added files.
        :return: None
        """
        return self.repository.add_files(directory, added_files)

    def remove_files(self, directory, removed_files):
        """
        Removes files from the index.
        :param directory: Any sub path in the repository.
        :param removed_files: The removed files
        :return: None
        """
        return self.repository.remove_files(directory, removed_files)

    def rename_files(self, directory, renamed_files):
        """
        Renames the files in the database
        :param directory: Any sub path in the repository.
        :param renamed_files: The renamed files
        :return: None
        """
        return self.repository.rename_files(directory, renamed_files)

    def modify_files(self, directory, modified_files):
        """
        Modifies the files in the database.
        :param directory: Any sub path in the repository.
        :param modified_files: The modified files.
        :return: None
        """
        return self.repository.modify_files(directory, modified_files)

    def stats(self, directory):
        """
        Returns stats for the database
        :param directory:  Any sub path in the repository.
        :return: The stats from the database.
        """
        return self.repository.stats(directory)
