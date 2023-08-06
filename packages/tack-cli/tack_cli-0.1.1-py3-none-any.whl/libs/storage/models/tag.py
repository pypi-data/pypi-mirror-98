from peewee import Model, CharField, ForeignKeyField, PrimaryKeyField

from .tag_type import TagType


class Tag(Model):
    """Representation of a tag in the database."""
    id = PrimaryKeyField()
    name = CharField(unique=True)
    type = ForeignKeyField(TagType, backref='tags', null=True)
