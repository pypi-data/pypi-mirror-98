from peewee import Model, CharField, PrimaryKeyField


class TagType(Model):
    """Database representation of the TagType"""
    id = PrimaryKeyField()
    name = CharField(unique=True)
