import asyncio
import logging
import os
import sys
import traceback
from time import time, sleep

from libs.containers import Adapters, Configs
from libs.plugin.loader import load_plugins


def set_log_level(str_level):
    """
    Sets the log level
    :param str_level: The log level to parse
    :return: None
    """
    mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    wanted_level = mapping.get(str_level.upper(), logging.INFO)
    logging.basicConfig(level=wanted_level)


set_log_level(os.environ.get('TACK_LOG_LEVEL', 'DEBUG'))

load_plugins()

cli_adapter = Adapters.cli_adapter()


def main_wrapper():
    """
    Wraps the main function in an asyncio run call
    :return: Nothing
    """
    time_start = time()
    (success, result) = asyncio.run(main())
    time_diff_ms = time() - time_start * 1000

    if time_diff_ms < 1000:
        sleep(1)

    if not success:
        error = result
        try:
            if error.error_code is not None:
                sys.exit(error.error_code)
            else:
                traceback.print_stack(error)
                sys.exit(1)
        except AttributeError:
            # traceback.print_stack(error)
            sys.exit(1)


async def main():
    """
    Main function that calls the cli adapter
    :return: Returns the result of the start function
    """
    Configs.config.override({
        'greeting': 'cheers mate',
    })

    return await cli_adapter.start()


if __name__ == '__main__':
    main_wrapper()
