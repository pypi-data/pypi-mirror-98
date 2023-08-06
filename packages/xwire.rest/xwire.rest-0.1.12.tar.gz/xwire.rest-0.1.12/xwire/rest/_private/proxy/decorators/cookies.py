from xwire.common import decorator_utils


def cookies(func):
    decorator_utils.set_decorator_metadata(func, cookies, {})
    return func
