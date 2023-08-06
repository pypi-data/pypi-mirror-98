import os
import configparser


config = configparser.ConfigParser()


def read_version():
    """
    Attempts to read the version from another ini file.
    :return: The parsed version as string
    """
    try:
        config.read(os.path.join(os.path.dirname(__file__), '..', '..', 'project.ini'))
        return config['Project']['Version']
    except KeyError:
        # This is for after packaging the files into the pyinstaller bundle which flattens the structure
        config.read(os.path.join(os.path.dirname(__file__), 'project.ini'))
        return config['Project']['Version']
