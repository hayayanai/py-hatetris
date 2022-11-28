import time
from functools import wraps


def watch(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time.perf_counter_ns()
        result = func(*args, **kargs)
        elapsed_time = time.perf_counter_ns() - start
        # print(f"{func.__name__} took {elapsed_time} ns")
        print(f"{func.__name__} {elapsed_time / 1000}")
        return result
    return wrapper
