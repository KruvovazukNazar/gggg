from functools import wraps


def even_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, int) and not isinstance(result, bool) and result % 2 == 0:
            print("Це парне число!")
        return result
    return wrapper
