from environs import Env


def parse():
    """
    Parses the environment variables.
    :return: The parsed env variables.
    """
    env = Env()

    is_machine_readable = env.bool('TACK_MACHINE', False)
    machine_mode = env('TACK_MACHINE_MODE', 'json')

    return {
        'is_machine_readable': is_machine_readable,
        'machine_mode': machine_mode
    }
