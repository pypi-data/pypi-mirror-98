from peewee import Model, ForeignKeyField

from .file import File
from .tag import Tag


# pylint: disable=too-few-public-methods
class TaggedFile(Model):
    """Database representation of TaggedFiles"""
    file = ForeignKeyField(File, backref='taggedfiles')
    tag = ForeignKeyField(Tag, backref='taggedfiles')

    class Meta:
        """Used for indexes in peewee"""
        indexes = (
            (('file', 'tag'), True),
        )
