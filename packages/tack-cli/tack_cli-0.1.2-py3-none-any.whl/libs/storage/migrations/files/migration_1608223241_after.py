from playhouse.migrate import TextField, SchemaMigrator, migrate


def migrate_up(migrator: SchemaMigrator):
    """
    Migrates the database to the correct schema.
    :param migrator: The migrator used to help us migrate things
    :return: None
    """
    migrate(
        migrator.add_column('tag', 'description', TextField(null=True)),
    )
