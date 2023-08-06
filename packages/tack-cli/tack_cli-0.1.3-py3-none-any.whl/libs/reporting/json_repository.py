import sys
import jsonpickle


class Repository:
    """The json repository to print json text"""
    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def print(obj):
        """
        Print the whole json object.
        :param obj: The object to print.
        :return: None
        """
        message_type = obj['type']

        if message_type == 'error':
            print(jsonpickle.dumps(obj), file=sys.stderr, flush=True)
        else:
            print(jsonpickle.dumps(obj), flush=True)
