from dependency_injector import providers, containers
from .storage.sqlite3_repository import Sqlite3Repository
from .storage.service import Service as StorageService
from .usecases.init_case import InitCase
from .usecases.use_case import UseCase
from .usecases.suggest import Suggest
from .cli.cli_adapter import CliAdapter
from .tag_operations.filesystem_repository import FilesystemRepository as TagOperationsFilesystemRepository
from .tag_operations.service import Service as TagService
from .suggestions.suggest_mp3_repository import SuggestMp3Repository
from .suggestions.file_path_repository import FilePathRepository as SuggestionFilePathRepository
from .suggestions.service import Service as SuggestionService
from .environment_variables import parsed as environment_variables
from .reporting.service import Service as ReportingService
from .reporting.stdout_repository import Repository as ReportingStdoutRepository
from .reporting.json_repository import Repository as ReportingJsonRepository
from .tack_meta.toml_repository import TomlRepository as TomlTackMetaRepository
from .tack_meta.service import TackMetaService
from .usecases.maintenance_use_case import MaintenanceUseCase
from .usecases.tag_use_case import TagUseCase
from .usecases.stats_case import StatsCase
from .plugin.loader import load_plugins


plugins = [providers.Factory(x) for x in load_plugins()]


# pylint: disable-msg=missing-class-docstring
class TackMeta(containers.DeclarativeContainer):
    toml_repository = providers.Factory(TomlTackMetaRepository)
    service = providers.Factory(TackMetaService, repository=toml_repository)


class Helpers(containers.DeclarativeContainer):
    common_variables = environment_variables.parse()


class Suggestions(containers.DeclarativeContainer):
    suggestions_mp3_repository = providers.Factory(SuggestMp3Repository)
    suggestions_file_path_repository = providers.Factory(SuggestionFilePathRepository)
    suggestions_service = providers.Factory(SuggestionService,
                                            providers.List(
                                                suggestions_mp3_repository,
                                                suggestions_file_path_repository
                                            ),
                                            TackMeta.service,
                                            *plugins)


class Reporting(containers.DeclarativeContainer):
    reporting_stdout_repository = providers.Factory(ReportingStdoutRepository)
    reporting_stdout_service = providers.Factory(ReportingService, repository=reporting_stdout_repository)
    reporting_json_repository = providers.Factory(ReportingJsonRepository)
    reporting_json_service = providers.Factory(ReportingService, repository=reporting_json_repository)
    reporting_service = reporting_json_service if Helpers.common_variables[
        'is_machine_readable'] else reporting_stdout_service


class TagOperations(containers.DeclarativeContainer):
    tag_operations_filesystem_repository = providers.Factory(TagOperationsFilesystemRepository,
                                                             reporting_service=Reporting.reporting_service)
    tag_operations_service = providers.Factory(TagService, repository=tag_operations_filesystem_repository)


class Storage(containers.DeclarativeContainer):
    sqlite3_repository = providers.Factory(Sqlite3Repository, tack_meta_service=TackMeta.service)
    sqlite3_service = providers.Factory(StorageService, repository=sqlite3_repository)


class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')


class UseCases(containers.DeclarativeContainer):
    init_case = providers.Singleton(InitCase, tack_meta_service=TackMeta.service,
                                    reporting_service=Reporting.reporting_service
                                    )
    use_case = providers.Singleton(UseCase,
                                   storage_service=Storage.sqlite3_service,
                                   tag_operations=TagOperations.tag_operations_service,
                                   reporting_service=Reporting.reporting_service,
                                   tack_meta_service=TackMeta.service)
    suggest_case = providers.Singleton(Suggest, storage_service=Storage.sqlite3_service,
                                       tag_operations=TagOperations.tag_operations_service,
                                       tag_suggestion=Suggestions.suggestions_service,
                                       reporting_service=Reporting.reporting_service,
                                       tack_meta_service=TackMeta.service)
    maintenance_case = providers.Singleton(MaintenanceUseCase, reporting_service=Reporting.reporting_service,
                                           tack_meta_service=TackMeta.service)
    tag_use_case = providers.Singleton(TagUseCase, reporting_service=Reporting.reporting_service,
                                       tack_meta_service=TackMeta.service,
                                       storage_service=Storage.sqlite3_service)
    stats_use_case = providers.Singleton(StatsCase,
                                         storage_service=Storage.sqlite3_service,
                                         tack_meta_service=TackMeta.service,
                                         reporting_service=Reporting.reporting_service)


class Adapters(containers.DeclarativeContainer):
    cli_adapter = providers.Singleton(CliAdapter,
                                      UseCases.init_case,
                                      UseCases.use_case,
                                      UseCases.suggest_case,
                                      Reporting.reporting_service,
                                      UseCases.maintenance_case,
                                      UseCases.tag_use_case,
                                      UseCases.stats_use_case,
                                      TackMeta.service,
                                      *plugins
                                      )
