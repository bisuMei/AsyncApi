import logging
import sys
import time
from functools import wraps


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """Wait for the connection services"""    
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = start_sleep_time
            while t < border_sleep_time:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    logger.error(error)
                    if t >= border_sleep_time:
                        raise error
                    time.sleep(t)
                    t = t * factor                    
        return inner
    return func_wrapper
