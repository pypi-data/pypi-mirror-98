def string_to_bool(some_string):
    """
    Transfers a simple string to boolean, considering the value it represents.
    :param some_string: The string value to convert.
    :return: A boolean indicating the value of the string
    :raises TypeError: When neither true, True, false or False are passed as parameter
    """
    if some_string in ('True', 'true'):
        return True

    if some_string in ('False', 'false'):
        return False

    raise TypeError(f'The passed string "{some_string}" is not a boolean')
