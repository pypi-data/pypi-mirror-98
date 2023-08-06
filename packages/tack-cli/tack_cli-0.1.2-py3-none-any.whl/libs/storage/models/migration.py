from peewee import Model, TextField, IntegerField


class Migration(Model):
    """
    A migration model that is used to represent them in the database.
    """
    epoch = IntegerField(unique=True, primary_key=True)
    title = TextField()
