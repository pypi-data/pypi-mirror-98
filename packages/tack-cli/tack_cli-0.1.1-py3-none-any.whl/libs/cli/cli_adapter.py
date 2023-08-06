from libs.exceptions.tack_repository_not_found_error import TackRepositoryNotFoundError
from libs.constants import ignored_matches
from .cli_args import parse


# pylint: disable-msg=too-many-branches
# pylint: disable-msg=too-many-return-statements
# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-instance-attributes
class CliAdapter:
    """The adapter to interface the cli"""

    def __init__(self,
                 init_case,
                 use_case,
                 suggest_case,
                 reporting_service,
                 maintenance_case,
                 tag_use_case,
                 stats_use_case,
                 metadata_service,
                 *plugins):
        self.init_case = init_case
        self.use_case = use_case
        self.suggest_case = suggest_case
        self.reporting_service = reporting_service
        self.maintenance_case = maintenance_case
        self.tag_use_case = tag_use_case
        self.stats_use_case = stats_use_case
        self.metadata_service = metadata_service
        self.plugins = plugins
        self.args = parse()

    def _extend_config(self, level, config=None):
        try:
            if config is None:
                config = self.metadata_service.create_or_read_defaults(level)

            for plugin in self.plugins:
                plugin_name = plugin.__class__.__name__

                plugin_default_config = plugin.default_config
                plugin_default_config.update({'enabled': True})
                config['plugins'][plugin_name] = plugin_default_config

            if 'ignored_matches' not in config:
                config['ignored_matches'] = ignored_matches

            self.metadata_service.create_defaults(level, config)
            return config
        except TackRepositoryNotFoundError:
            return {}

    async def _start_wrapped(self):
        system_config = self._extend_config('system')
        self._extend_config('user', system_config)

        if self.args.subs == 'init':
            init_result = await self.init_case.action_init(self.args.directory)
            return init_result

        if self.args.subs == 'stats':
            return await self.stats_use_case.action_stats(self.args.directory)

        if self.args.subs == 'settings':
            if self.args.settings_subs == 'list':
                return await self.maintenance_case.action_setting_list(self.args.directory)
            if self.args.settings_subs == 'set':
                opts = {
                    'key': self.args.key,
                    'value': self.args.value,
                }
                return await self.maintenance_case.action_set_setting(self.args.directory, opts)
            if self.args.settings_subs == 'unset':
                opts = {
                    'key': self.args.key,
                }
                return await self.maintenance_case.action_unset_setting(self.args.directory, opts)

        if self.args.subs == 'maintenance':
            if self.args.maintenance_subs == 'integrity':
                return await self.maintenance_case.action_maintenance_integrity(self.args.directory)
            if self.args.maintenance_subs == 'matcher':
                if self.args.maintenance_matcher_subs == 'list':
                    return await self.maintenance_case.action_maintenance_matcher_list(self.args.directory)
                if self.args.maintenance_matcher_subs == 'add':
                    return await self.maintenance_case.action_maintenance_matcher_add(self.args.directory,
                                                                                      self.args.match)
                if self.args.maintenance_matcher_subs == 'remove':
                    return await self.maintenance_case.action_maintenance_matcher_remove(self.args.directory,
                                                                                         self.args.match)
                if self.args.maintenance_matcher_subs == 'restore':
                    return await self.maintenance_case.action_maintenance_matcher_restore(self.args.directory)

        if self.args.subs == 'refresh':
            return await self.use_case.action_refresh(self.args.directory)

        if self.args.subs == 'tag':
            if self.args.tag_subs == 'find':
                if self.args.tag_find_subs == 'untagged':
                    return await self.tag_use_case.action_find_untagged(self.args.directory, self.args.file_match)
                if self.args.tag_find_subs == 'tags':
                    return await self.tag_use_case.action_find_tags(self.args.directory,
                                                                    self.args.with_files,
                                                                    self.args.in_here,
                                                                    self.args.tags)
                if self.args.tag_find_subs == 'by-tag':
                    return await self.tag_use_case.action_find_tagged_files(self.args.directory, self.args.tags)
                if self.args.tag_find_subs == 'by-file':
                    return await self.tag_use_case.action_find_files_with_tag(self.args.directory, self.args.file_match)
            if self.args.tag_subs == 'add':
                return await self.tag_use_case.action_add_tags(self.args.directory, self.args.tags, self.args.type)
            if self.args.tag_subs == 'rename':
                return await self.tag_use_case.action_rename_tag(self.args.directory, self.args.tag, self.args.name)
            if self.args.tag_subs == 'delete':
                opts = {
                    'tags': self.args.tags,
                    'tags_list': self.args.tags_list,
                }
                return await self.tag_use_case.action_delete_tags(self.args.directory, opts)
            if self.args.tag_subs == 'suggest':
                return await self.suggest_case.suggest_tag(self.args.directory, self.args.file_match, self.args.apply,
                                                           self.args.detailed)
            if self.args.tag_subs == 'file':
                opts = {
                    'tags': self.args.tags,
                    'tags_list': self.args.tags_list,
                    'file_match': self.args.file_match,
                    'file_list': self.args.file_list,
                }
                return await self.tag_use_case.action_tag_files(self.args.directory, opts)
            if self.args.tag_subs == 'list':
                return await self.tag_use_case.action_find_tags(self.args.directory, False, False, [])
        if self.args.subs == 'untag':
            if self.args.untag_subs == 'file':
                options = {
                    'tags': self.args.tags,
                    'file_match': self.args.file_match,
                    'file_list': self.args.file_list,
                }
                return await self.tag_use_case.action_untag_files(self.args.directory, options)
        if self.args.subs == 'list':
            if self.args.list_subs == 'files':
                return await self.use_case.action_list_files(self.args.directory)

    async def start(self):
        """
        Starts the cli operations.
        :return: None
        """

        try:
            result = await self._start_wrapped()
            return True, result

        except Exception as err:  # pylint: disable-msg=broad-except
            structure_to_print = {
                'type': 'error',
                'error_name': err.__class__.__name__,
                'message': str(err)
            }
            self.reporting_service.print(structure_to_print)
            return False, err
