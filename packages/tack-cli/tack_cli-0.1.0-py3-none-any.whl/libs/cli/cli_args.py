import argparse

from helpers import read_version

version = read_version()


# pylint: disable-msg=too-many-locals
# pylint: disable-msg=too-many-statements
def parse():
    """
    Parses the CLI parameters on call.
    :return: Returns the parsed parameters and returns a dictionary.
    """
    parser = argparse.ArgumentParser(description='Tagging core to allow to tag files.')
    parser.add_argument('--version', action='version', version=version)
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='Choose a subcommand to perform a specific task.',
                                       dest='subs',
                                       required=True)

    refresh_parser = subparsers.add_parser('refresh', help='Refreshes the file index.')
    refresh_parser.add_argument('--directory',
                                help='Specify the directory you want to execute the command on.',
                                default='.')

    init_parser = subparsers.add_parser('init', help='Initializes the tagging repository in the current directory.')
    init_parser.add_argument('--directory',
                             help='Specify the directory you want to execute the command on.',
                             default='.')

    stats_parser = subparsers.add_parser('stats', help='Shows statistics for the repository.')
    stats_parser.add_argument('--directory',
                              help='Specify the directory you want to execute the command on.',
                              default='.')

    list_parser = subparsers.add_parser('list', help='Lists things in a directory.')
    list_subparsers = list_parser.add_subparsers(title='list_subcommands', dest='list_subs', required=True)

    list_files_parser = list_subparsers.add_parser('files', help='Lists files')
    list_files_parser.add_argument('--directory',
                                   help='Specify the directory you want to execute the command on.',
                                   default='.')

    settings_parser = subparsers.add_parser('settings', help='Performs settings adjustments')
    settings_subparsers = settings_parser.add_subparsers(dest='settings_subs', required=True)
    settings_list_parser = settings_subparsers.add_parser('list',
                                                          help='Lists all available settings')
    settings_list_parser.add_argument('--directory',
                                      help='Specify the directory you want to execute the command on.',
                                      default='.')
    settings_set_parser = settings_subparsers.add_parser('set',
                                                         help='Sets a config attribute for that plugin.')
    settings_set_parser.add_argument('--directory',
                                     help='Specify the directory you want to execute the command on.',
                                     default='.')
    settings_set_parser.add_argument('--key',
                                     help='Specify the key of the setting you\'some_dict like to set',
                                     required=True)
    settings_set_parser.add_argument('--value',
                                     help='Specify the key of the setting you\'some_dict like to set',
                                     required=True)
    settings_unset_parser = settings_subparsers.add_parser('unset',
                                                           help='Unsets a config attribute for that '
                                                                'plugin.')
    settings_unset_parser.add_argument('--directory',
                                       help='Specify the directory you want to execute the command on.',
                                       default='.')
    settings_unset_parser.add_argument('--key',
                                       help='Specify the key of the setting you\'some_dict like to set',
                                       required=True)

    maintenance_parser = subparsers.add_parser('maintenance', help='Perform maintenance actions')
    maintenance_subparsers = maintenance_parser.add_subparsers(dest='maintenance_subs', required=True)
    maintenance_integrity_parser = maintenance_subparsers.add_parser('integrity',
                                                                     help='Checks the integrity of the repository.')
    maintenance_integrity_parser.add_argument('--directory',
                                              help='Specify the directory you want to execute the command on.',
                                              default='.')
    maintenance_matcher = maintenance_subparsers.add_parser('matcher',
                                                            help='Handles the matches of the repository.')
    maintenance_matcher_subparsers = maintenance_matcher.add_subparsers(dest='maintenance_matcher_subs', required=True)
    maintenance_matcher_list = maintenance_matcher_subparsers.add_parser(
        'list',
        help='Lists all the ignored matchers in the repository.')
    maintenance_matcher_list.add_argument('--directory',
                                          help='Specify the directory you want to execute the command on.',
                                          default='.')
    maintenance_matcher_add = maintenance_matcher_subparsers.add_parser('add',
                                                                        help='Adds a new matcher in the repository.')
    maintenance_matcher_add.add_argument('--directory',
                                         help='Specify the directory you want to execute the command on.',
                                         default='.')
    maintenance_matcher_add.add_argument('--match',
                                         help='Specify the match you\'some_dict like to add to the matchers.')
    maintenance_matcher_remove = maintenance_matcher_subparsers.add_parser('remove',
                                                                           help='Removes a match in the repository.')
    maintenance_matcher_remove.add_argument('--directory',
                                            help='Specify the directory you want to execute the command on.',
                                            default='.')
    maintenance_matcher_remove.add_argument('--match',
                                            dest='match',
                                            help='Specify the match you\'some_dict like to remove.')

    maintenance_matcher_restore = maintenance_matcher_subparsers.add_parser(
        'restore',
        help='Restores the default metches in the repository.')
    maintenance_matcher_restore.add_argument('--directory',
                                             help='Specify the directory you want to execute the command on.',
                                             default='.')

    tag_parser = subparsers.add_parser('tag', help='Tags files based on a specific match')
    tag_subparsers = tag_parser.add_subparsers(dest='tag_subs', required=True)
    tag_find_parser = tag_subparsers.add_parser('find', help='Finds something based on a tag.')
    tag_find_subparser = tag_find_parser.add_subparsers(dest='tag_find_subs', required=True)
    tag_find_untagged = tag_find_subparser.add_parser('untagged')
    tag_find_untagged.add_argument('--directory',
                                   help='Specify the directory you want to execute the command on.',
                                   default='.')
    tag_find_untagged.add_argument('--file_match', help='Specify a partial text of the file path.')
    tag_find_by_tag = tag_find_subparser.add_parser('by-tag')
    tag_find_by_tag.add_argument('--directory',
                                 help='Specify the directory you want to execute the command on.',
                                 default='.')
    tag_find_by_tag.add_argument('--tag',
                                 dest='tags',
                                 action='append',
                                 default=[],
                                 help='Specifies the tag(s) you want to use to find files. Supports multiple tags for '
                                      'logical combinations.')
    tag_find_by_file = tag_find_subparser.add_parser('by-file')
    tag_find_by_file.add_argument('--directory',
                                  help='Specify the directory you want to execute the command on.',
                                  default='.')
    tag_find_by_file.add_argument('--file_match', help='Specifies the files you want to find.', default=None)
    tag_find_tags = tag_find_subparser.add_parser('tags')
    tag_find_tags.add_argument('--directory',
                               help='Specify the directory you want to execute the command on.',
                               default='.')
    tag_find_tags.add_argument('--files', action='store_true', dest='with_files')
    tag_find_tags.add_argument('--here',
                               action='store_true',
                               dest='in_here',
                               help='Specify whether or not to consider tags in the currently active directory')
    tag_find_tags.add_argument('--tag',
                               dest='tags',
                               action='append',
                               default=[],
                               help='Specifies the tag(s) you want to use to find files. Supports multiple tags for '
                                    'logical combinations.')
    tag_rename_parser = tag_subparsers.add_parser('rename', help='Renames a tag in the repository.')
    tag_rename_parser.add_argument('--directory',
                                   help='Specify the directory you want to execute the command on.',
                                   default='.')
    tag_rename_parser.add_argument('--tag', dest='tag', help='The tag you want to rename.',
                                   required=True)
    tag_rename_parser.add_argument('--name', dest='name', help='The new name of the tag.',
                                   required=False)
    tag_add_parser = tag_subparsers.add_parser('add', help='Adds a tag to the repository.')
    tag_add_parser.add_argument('--directory',
                                help='Specify the directory you want to execute the command on.',
                                default='.')
    tag_add_parser.add_argument('--tag', action='append', dest='tags', help='The tags you want to create.',
                                required=True)
    tag_add_parser.add_argument('--type', dest='type', help='The type of tag you want to create.',
                                default='custom',
                                required=False)
    tag_delete_parser = tag_subparsers.add_parser('delete', help='Deletes a tag from the repository.')
    tag_delete_parser.add_argument('--directory',
                                   help='Specify the directory you want to execute the command on.',
                                   default='.')
    tag_delete_parser.add_argument('--tag', dest='tags', action='append',
                                   help='The tags you want to delete from the repository.', required=False)
    tag_delete_parser.add_argument('--tags_list', help='Specify the path to file that contains all file references.',
                                   required=False)
    tag_suggest_parser = tag_subparsers.add_parser('suggest', help='Suggests tags for a specified file')
    tag_suggest_parser.add_argument('--directory',
                                    help='Specify the directory you want to execute the command on.',
                                    default='.')
    tag_suggest_parser.add_argument('--file_match', help='Specify a partial text of the file path.', default=None)
    tag_suggest_parser.add_argument('--detailed', action='store_true', help='Suggest tags with detailed reason.')
    tag_suggest_parser.add_argument('--apply', action='store_true', help='Apply the suggestions.')
    tag_file_parser = tag_subparsers.add_parser('file', help='Tags a specified file.')
    tag_file_parser.add_argument('--directory',
                                 help='Specify the directory you want to execute the command on.',
                                 default='.')
    tag_file_parser.add_argument('--tag', dest='tags', action='append',
                                 help='The tags you want to associate with the matched files.', required=False)
    tag_file_parser.add_argument('--file_match', help='Specify a partial text of the file path.', default=None)
    tag_file_parser.add_argument('--file_list', help='Specify the path to file that contains all file references.',
                                 required=False)
    tag_file_parser.add_argument('--tags_list', help='Specify the path to file that contains all file references.',
                                 required=False)

    tag_list_parser = tag_subparsers.add_parser('list', help='Lists all tags of the repository.')
    tag_list_parser.add_argument('--directory',
                                 help='Specify the directory you want to execute the command on.',
                                 default='.')

    untag_parser = subparsers.add_parser('untag', help='Untags files based on a specific match')
    untag_subparsers = untag_parser.add_subparsers(dest='untag_subs', required=True)
    untag_file_parser = untag_subparsers.add_parser('file', help='Untags a specified file.')
    untag_file_parser.add_argument('--directory',
                                   help='Specify the directory you want to execute the command on.',
                                   default='.')
    untag_file_parser.add_argument('--tag', dest='tags', action='append',
                                   help='The tags you want to disassociate with the matched files.', required=True)
    untag_file_parser.add_argument('--file_match', help='Specify a partial text of the file path.', required=False)
    untag_file_parser.add_argument('--file_list', help='Specify the path to file that contains all file references.',
                                   required=False)

    return parser.parse_args()
