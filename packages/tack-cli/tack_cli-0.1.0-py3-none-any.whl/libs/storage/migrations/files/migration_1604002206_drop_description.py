from playhouse.migrate import SchemaMigrator, migrate


def migrate_up(migrator: SchemaMigrator):
    """
    Migrates the database to the correct schema.
    :param migrator: The migrator used to help us migrate things
    :return: None
    """
    migrate(
        migrator.drop_column('tag', 'description'),
    )
