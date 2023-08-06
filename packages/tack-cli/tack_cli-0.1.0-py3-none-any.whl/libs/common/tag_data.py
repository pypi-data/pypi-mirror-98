class TagData:
    """
    Defines the attributes associated with the tag data.
    """
    def __init__(self, name, tag_type, origin=None, operation_succeeded=False):
        """
        Initializes the tag with prefilled data.
        :param name: The name of the tag.
        :param tag_type: The type of the tag.
        :param origin: Origin of the tag.
        :param operation_succeeded: Whether the operation was successful or not.
        """
        self._name = name
        self._type = tag_type
        self._origin = origin
        self._operation_succeeded = operation_succeeded

    @property
    def name(self) -> str:
        """
        Returns the tag name.
        """
        return self._name

    @property
    def type(self) -> str:
        """
        Specifies the type of the tag.
        """
        return self._type

    @property
    def origin(self) -> str:
        """
        Specifies the origin of the tag, like mp3, mkv, date, etc.
        """
        return self._origin

    @property
    def operation_succeeded(self) -> bool:
        """
        Specifies if the operation was successful or not (depends on the context!)
        :return: Either True or False.
        """
        return self._operation_succeeded

    @operation_succeeded.setter
    def operation_succeeded(self, operation_succeeded: bool):
        self._operation_succeeded = operation_succeeded

    def _key(self):
        return self._name + self._type

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        if isinstance(other, TagData):
            return self._key() == other._key()

        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f'{self._type}: {self._name}'

    def __lt__(self, other):
        return self._name < other._name

    def to_dict(self):
        """
        Transforms the current object to a doctionary.
        :return: A dictionary containing all the data.
        """
        return {
            'name': self._name,
            'type': self._type,
            'origin': self.origin,
            'operation_succeeded': self._operation_succeeded
        }
