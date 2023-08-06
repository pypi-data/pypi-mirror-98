from libs.common.file_data import FileData


class FileDataPath(FileData):
    """
    The data path file - without the contents.
    """

    def __init__(self, file_data):
        self._valid_args = ['path']
        self._storage['path'] = file_data.path
        super().__init__()
