import requests
import re
from typing import Callable, TypeVar, get_type_hints, Type
import xwire.transport
from xwire.common import decorator_utils
from xwire.rest._private.utils import get_cookies, get_headers
from xwire.rest._private.proxy.decorators import resource


T = TypeVar('T')


def _do_get(url: str, return_class: Type[T], **kwargs) -> T:
    response = requests.get(url, timeout=5, **kwargs)
    if response.status_code >= 400:
        response.raise_for_status()
    elif return_class is not None:
        return xwire.transport.json.deserialize(response.json(), return_class)
    else:
        return None


def get(path: str):
    path_params = re.findall(r':\w+', path)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        return_type = get_type_hints(func)['return']

        def wrapper(self, *args):
            resource_metadata = decorator_utils.get_decorator_metadata(self, resource)

            method_path = path
            for path_param, arg in zip(path_params, args):
                method_path = method_path.replace(path_param, str(arg))

            url = self.base_url + resource_metadata['resource_path'] + method_path
            return _do_get(url, return_type, cookies=get_cookies(self), headers=get_headers(self))

        return wrapper
    return decorator
