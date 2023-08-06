from abc import abstractmethod, ABC


class BasePlugin(ABC):
    """
    Base structure for the Plugin structure
    """
    __extendable_repositories = [
        'SuggestRepository'
    ]

    def __init__(self):
        super().__init__()

        if self.extends_repository not in BasePlugin.__extendable_repositories:
            raise TypeError(f'The repository "{self.extends_repository}" is not greenlighted for extending')

    @property
    @abstractmethod
    def author(self):
        """
        The author's name
        :return: String
        """

    @property
    @abstractmethod
    def description(self):
        """
        A generic description about what your plugin does.
        :return: String
        """

    @property
    @abstractmethod
    def extends_repository(self):
        """
        The repository you want to extend. It's a whitelist.
        :return: The name of the repository you want to extend.
        """

    @property
    @abstractmethod
    def default_config(self):
        """
        The default config for the plugin itself.
        :return: A dictionary with config elements
        """

    @abstractmethod
    def process(self, **kwargs):
        """
        The method that actually handles something. Entrypoint.
        :param kwargs: The parameters that are passed to the function. It differs per call so have a look at it!
        :return: Returns whatever API you are implementing.
        """
