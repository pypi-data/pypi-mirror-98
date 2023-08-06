import functools
import time
import logging
import asyncio


def timeit(func):
    """
    Decorator to measure the time a function takes to execute.
    :param func: The function that is measured.
    :return: Returns the result of the called function.
    """
    @functools.wraps(func)
    async def timed(*args, **kw):
        time_start = time.time()

        is_coroutine = asyncio.iscoroutinefunction(func)
        logging.debug('is coroutine (%s): %s', func.__name__, is_coroutine)

        result = await func(*args, **kw) if asyncio.iscoroutinefunction(func) else func(*args, **kw)
        time_end = time.time()

        time_in_ms = (time_end - time_start) * 1000
        human = _human_time_duration(time_in_ms)
        logging.debug('%s: %s', func.__name__, human)

        return result

    return timed


TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7 * 1000),
    ('day', 60 * 60 * 24 * 1000),
    ('hour', 60 * 60 * 1000),
    ('min', 60 * 1000),
    ('sec', 1000),
    ('milli', 1)
)


def _human_time_duration(duration_in_ms):
    if duration_in_ms == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, duration_in_ms = divmod(int(duration_in_ms), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
