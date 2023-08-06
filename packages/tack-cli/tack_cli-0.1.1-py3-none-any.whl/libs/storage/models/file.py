from peewee import Model, TextField, BigIntegerField, IntegerField, CharField, PrimaryKeyField


class File(Model):
    """
    A simple class to hold a files attributes.
    """
    id = PrimaryKeyField()
    path = TextField(unique=True)
    modify_time = BigIntegerField()
    create_time = BigIntegerField()
    size = IntegerField()
    fingerprint = CharField()
