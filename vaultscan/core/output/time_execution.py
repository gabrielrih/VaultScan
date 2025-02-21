import time
import functools

from vaultscan.core.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


def time_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.debug(f"{func.__name__} finished in {end - start:.4f} seconds")
        return result
    return wrapper
