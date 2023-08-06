from playhouse.migrate import TextField, SchemaMigrator, migrate, BigIntegerField, IntegerField, CharField, SQL


def migrate_up(migrator: SchemaMigrator):
    """
    Migrates the database to the correct schema.
    :param migrator: The migrator used to help us migrate things
    :return: None
    """
    migrator.database.execute_sql('CREATE TABLE IF NOT EXISTS file(id INTEGER NOT NULL PRIMARY KEY);')
    migrator.database.execute_sql('CREATE TABLE IF NOT EXISTS tagtype(id INTEGER NOT NULL PRIMARY KEY);')
    migrator.database.execute_sql('CREATE TABLE IF NOT EXISTS tag(id INTEGER NOT NULL PRIMARY KEY);')
    migrator.database.execute_sql('CREATE TABLE IF NOT EXISTS taggedfile(id INTEGER NOT NULL PRIMARY KEY);')
    migrate(
        migrator.add_column('file', 'path', TextField(unique=True, default='')),
        migrator.add_column('file', 'modify_time', BigIntegerField(default=0)),
        migrator.add_column('file', 'create_time', BigIntegerField(default=0)),
        migrator.add_column('file', 'size', IntegerField(default=0)),
        migrator.add_column('file', 'fingerprint', CharField(default='')),

        migrator.add_column('tagtype', 'name', CharField(unique=True, default='')),

        migrator.add_column('tag', 'name', CharField(unique=True, default='default')),
        migrator.add_column('tag', 'type_id', IntegerField(null=True, constraints=[SQL('REFERENCES tagtype(id)')])),

        migrator.add_column('taggedfile', 'file_id', IntegerField(null=True, constraints=[SQL('REFERENCES file(id)')])),
        migrator.add_column('taggedfile', 'tag_id', IntegerField(null=True, constraints=[SQL('REFERENCES tag(id)')])),
    )
