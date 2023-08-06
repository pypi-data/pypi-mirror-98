from xwire.common import decorator_utils


def headers(func):
    decorator_utils.set_decorator_metadata(func, headers, {})
    return func
