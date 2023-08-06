import collections
import sys


class Repository:
    """The stdout repository to print."""

    def __init__(self):
        self._lookup = {
            'init': self._print_initialize_repository,
            'add_tags': self._print_add_tags,
            'rename_tag': self._print_rename_tag,
            'delete_tags': self._print_delete_tags,
            'find_untagged': self._print_find_untagged,
            'maintenance_integrity': self._print_maintenance_integrity,
            'list_files': self._print_list_files,
            'find_tagged_files': self._print_tagged_files,
            'find_files_with_tag': self._print_files_with_tag,
            'matcher_list': self._print_matcher_list,
            'matcher_add': self._print_matcher_add,
            'matcher_remove': self._print_matcher_remove,
            'tag_files': self._print_tag_files,
            'refresh': self._print_refresh,
            'find_tags': self._print_find_tags,
            'suggest': self._print_suggest,
            'error': self._print_error,
            'matcher_restore': self._print_matcher_restore,
            'progress': self._print_progress,
            'stats': self._print_stats,
            'setting_list': self._print_setting_list,
            'set_setting': self._print_setting_set,
            'unset_setting': self._print_setting_unset,
        }

    def __str__(self):
        return self.__class__.__name__

    def print(self, obj):
        """
        Prints stuff to the console
        :param obj: The object to print.
        :return: None
        """
        try:
            some_function = self._lookup[obj['type']]
            return some_function(obj)
        except KeyError as exc:
            raise Exception(f'Specified type not found ({obj["type"]})') from exc

    @staticmethod
    def _flatten_settings(some_dict, parent_key='', sep='_'):
        """
        Flattens a dictionary to a string
        Stolen from: https://stackoverflow.com/a/6027615/2670428
        :param some_dict:
        :param parent_key:
        :param sep:
        :return:
        """
        items = []
        for key, value in some_dict.items():
            new_key = parent_key + sep + key if parent_key else key
            if isinstance(value, collections.MutableMapping):
                items.extend(Repository._flatten_settings(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
        return dict(items)

    @staticmethod
    def _print_setting_set(obj):
        settings = obj['config']['settings']
        flattened = Repository._flatten_settings(settings, sep='.')
        for key, value in flattened.items():
            print(f'{key}: {value}')

    @staticmethod
    def _print_setting_unset(obj):
        settings = obj['config']['settings']
        flattened = Repository._flatten_settings(settings, sep='.')
        for key, value in flattened.items():
            print(f'{key}: {value}')

    @staticmethod
    def _print_setting_list(obj):
        print('settings:')
        Repository._print_dict_entries(obj['settings'], 1)

    @staticmethod
    def _print_dict_entries(obj, depth=0):
        for key, value in obj.items():
            indention = '\t' * depth
            if isinstance(value, dict):
                print(f'{indention}{key}:')
                Repository._print_dict_entries(value, depth + 1)
            else:
                print(f'{indention}{key}: {value}')

    @staticmethod
    def _print_initialize_repository(obj):
        prefix = 'Initialized empty' if obj['is_new_repository'] else 'Reinitialized'
        print(f'{prefix} Tack repository in {obj["target_folder"]}')

    @staticmethod
    def _print_add_tags(obj):
        for handled_tag in obj['handled_tags']:
            tag_name = f'{handled_tag["name"]} ({handled_tag["type"]})'
            print(handled_tag)
            if handled_tag['operation_succeeded']:
                print(f'Created tag "{tag_name}".')
            else:
                print(f'Tag "{tag_name}" already exists.')

    @staticmethod
    def _print_delete_tags(obj):
        print(f'Successfully deleted {len(obj["deleted_tags"])} tags')
        for tag in obj['deleted_tags']:
            print(f'  * "{tag}"')

    @staticmethod
    def _print_find_untagged(obj):
        print('Files with no tag:')
        for untagged_file in obj['untagged_files']:
            print(untagged_file)

        print(f'TOTAL: {len(obj["untagged_files"])}')

    @staticmethod
    def _print_maintenance_integrity(obj):
        if obj['integrity_in_tact']:
            print('Integrity of repository in tact!')
            return

        if obj['integrity_was_fixed']:
            print(f'Fixed integrity in for repository in repo: {obj["repo_path"]}')
            return

        print(
            'Integrity of repository broken. Calculated: {} In Repo: {}'
            .format(
                obj["database_integrity"],
                obj["saved_integrity"]
            )
        )

    @staticmethod
    def _print_list_files(obj):
        for file in obj['files']:
            print(file['path'])

    @staticmethod
    def _print_tagged_files(obj):
        print(f'{" + ".join(obj["tags"])} ({len(obj["tagged_files"])}):')
        for tagged_file in obj['tagged_files']:
            print(f'\t{tagged_file}')

    @staticmethod
    def _print_files_with_tag(obj):
        for entry in obj['files_with_tags']:
            file = entry['file']
            tags = entry['tags']
            print(f'{file["path"]} ({len(tags)})')
            for tag in tags:
                print(f'\t{tag}')

    @staticmethod
    def _print_matcher_list(obj):
        max_width_for_index = len(str(len(obj['ignored_matches'])))
        for index, ignored_match in enumerate(obj['ignored_matches']):
            print(f'[{index:0{max_width_for_index}}] {ignored_match}')

    @staticmethod
    def _print_matcher_add(obj):
        if obj['success']:
            print(f'Successfully added entry {obj["match"]}')
        else:
            print(f'Could not add item "{obj["match"]}" because it was already included.')

    @staticmethod
    def _print_matcher_remove(obj):
        delete_confirmation = obj['delete_confirmation']
        if obj['success'] is True:
            print(
                'successfully removed index [{}] ({}) from repository.'
                .format(
                    delete_confirmation["index"],
                    delete_confirmation["item"],
                )
            )
        else:
            print(delete_confirmation)

    @staticmethod
    def _print_tag_files(obj):
        for entry in obj['data']:
            print(f'associated file {entry["file"]["path"]} with tag {entry["tag"]["name"]} ({entry["tag"]["type"]})')

    @staticmethod
    def _print_refresh(obj):
        if obj['changed']:
            print(f'File on filesystem: {obj["files_on_fs"]}')
            print(f'Files in index:     {obj["files_on_index"]}')
            print(f'Added files:        {obj["added_files"]}')
            print(f'Removed files:      {obj["removed_files"]}')
            print(f'Renamed files:      {obj["renamed_files"]}')
            print(f'Modified files:     {obj["modified_files"]}')
        else:
            print('No change detected.')

    @staticmethod
    def _print_find_tags(obj):
        for tag, files in obj['tags'].items():
            print(f'{tag} ({len(files)})')

            if obj['show_files']:
                for file in files:
                    print(f'\t{file}')

    @staticmethod
    def _print_error(obj):
        print(str(obj['message']), file=sys.stderr, flush=True)

    @staticmethod
    def _print_suggest(obj):
        for file in obj['files']:
            print(f'Suggestion for "{file["path"]}"')
            for tag in file['tags']:
                print(f' * {tag}')

        print(f'Unknown tags ({len(obj["unknown_tags"])}):')
        for unknown_tag in obj['unknown_tags']:
            print(f' * {unknown_tag}')

        print(f'Untagged files ({len(obj["untagged_files"])}):')
        for untagged_file in obj['untagged_files']:
            print(f' * {untagged_file}')

    @staticmethod
    def _print_rename_tag(obj):
        if obj['renamed_tag']['renamed']:
            print(f'Renamed {obj["renamed_tag"]["old_name"]} -> {obj["renamed_tag"]["new_name"]}')
        else:
            print(f'Did not rename tag {obj["renamed_tag"]["old_name"]} ({obj["renamed_tag"]["reason"]})')

    @staticmethod
    def _print_matcher_restore(obj):
        matches = obj['matches']
        print(f'Restored {len(matches)} matches:')
        for match in matches:
            print(f'* {match}')

    @staticmethod
    def _print_progress(obj):
        print(f'progress: {obj["progress"]}%')

    @staticmethod
    def _print_stats(obj):
        print('Repository')
        print('==========')
        print(f'Path:            {obj["repository"]["path"]}')
        print(f'Creation:        {obj["repository"]["config"]["creation"]}')
        print(f'Storage:         {obj["repository"]["config"]["storage"]}')
        print(f'Ignored Matches: {obj["repository"]["config"]["ignored_matches"]}')
        print(f'Integrity:       {obj["repository"]["config"]["integrity"]["database"]}')
        print('Database')
        print('========')
        print(f'Tags:            {obj["database"]["tag_count"]}')
        print(f'Files:           {obj["database"]["file_count"]}')
        print(f'Associations:    {obj["database"]["associations"]}')
        print(f'Size:            {obj["database"]["size"]}')
