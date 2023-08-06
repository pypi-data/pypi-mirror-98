class Service:
    """The reporting service"""
    def __init__(self, repository):
        self.repository = repository

    def __str__(self):
        return self.__class__.__name__

    def print(self, obj):
        """
        Prints anything.
        :param obj: The object to print.
        :return: None
        """
        return self.repository.print(obj)
