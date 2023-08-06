class FileData:
    """Keep all file data available for easier access"""
    input_args = ['path', 'suggested_tags', 'fingerprint', 'size', 'modify_time', 'create_time', 'new_path',
                  'new_create_time']
    key_args = input_args

    def __init__(self, **kwargs):
        self._storage = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in FileData.input_args:
                    self._storage[key] = value

    def to_dict(self):
        """
        Transforms the object to a simple dictionary
        :return: {}
        """
        return self._storage

    @staticmethod
    def set_key_args(key_args, existing_set=None):
        """
        Sets the arguments that make up the unique key for this structure.
        :param key_args: The list or arguments that make up the keys.
        :param existing_set: Re-hashes the set if specified.
        :return: Returns a new set of the data to re-hash.
        """
        FileData.key_args = key_args
        if existing_set is None:
            return set()

        return set(existing_set)

    @property
    def path(self):
        """Returns the path of the file"""
        return self._storage['path']

    @property
    def new_create_time(self):
        """Returns the new create time of the file (renaming)"""
        return self._storage['new_create_time']

    @new_create_time.setter
    def new_create_time(self, new_create_time):
        """Sets the new create time of the file (renaming)"""
        self._storage['new_create_time'] = new_create_time

    @property
    def new_path(self):
        """Returns the new path of the file (renaming)"""
        try:
            return self._storage['new_path']
        except KeyError:
            return ''

    @new_path.setter
    def new_path(self, new_path):
        """Sets the new path of the file (renaming)"""
        self._storage['new_path'] = new_path

    @property
    def fingerprint(self):
        """Returns the fingerprint of the file"""
        return self._storage['fingerprint']

    @fingerprint.setter
    def fingerprint(self, finger):
        """Sets the fingerprint of the file"""
        self._storage['fingerprint'] = finger

    @property
    def create_time(self):
        """Returns the create time of the file"""
        return self._storage['create_time']

    @property
    def modify_time(self):
        """Returns the modify time of the file"""
        return self._storage['modify_time']

    @property
    def size(self):
        """Returns the size of the file"""
        return self._storage["size"]

    @property
    def suggested_tags(self):
        """Returns a list of suggested tags"""
        return self._storage['suggested_tags']

    def key(self):
        """
        Returns the key that specifies what makes this structure unique.
        :return: A string with all keys concat.
        """
        return ''.join([str(self._storage[key_arg]) for key_arg in FileData.key_args])

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        if isinstance(other, FileData):
            return self.key() == other.key()

        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):

        if len(self.new_path) > 0:
            path_str = f'{self._storage["path"]} -> {self._storage["new_path"]}'
        else:
            path_str = f'{self._storage["path"]}'

        size = self._storage["size"]
        modify_time = self._storage["modify_time"]
        create_time = self._storage["create_time"]

        return f'{path_str} ({size}, {modify_time}, {create_time}) [{self.fingerprint}]'
