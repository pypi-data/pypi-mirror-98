def find(array, condition):
    """
    Finds the first element that matches the passed condition.
    :param array: The array you want to search through.
    :param condition: Any condition that is applied to each element in the array.
    :return: (found, element)
    """
    for element in array:
        if condition(element):
            return True, element

    return False, None


def chunk(array, size):
    """
    Chunks an array into the specified size
    :param array: The array to slice up
    :param size: The size each created array should have.
    :return: Returns a list of arrays containing a specified amount of entries.
    """
    for idx in range(0, len(array), size):
        yield array[idx:idx + size]
