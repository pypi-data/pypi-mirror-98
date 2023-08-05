import requests
from typing import Dict, Type, TypeVar, get_type_hints, Callable
import xwire.transport
from xwire.common import decorator_utils
from xwire.rest._private.proxy.decorators import resource
from xwire.rest._private.utils import get_cookies, get_headers

T = TypeVar('T')


def _do_post(url: str, json: Dict[str, str], return_class: Type[T], **kwargs) -> T:
    response = requests.post(url, json=json, timeout=5, **kwargs)
    if response.status_code >= 400:
        response.raise_for_status()
    elif return_class is not None:
        return xwire.transport.json.deserialize(response.json(), return_class)
    else:
        return None


def post(path: str):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        return_type = get_type_hints(func)['return']

        def wrapper(self, *args):
            resource_metadata = decorator_utils.get_decorator_metadata(self, resource)
            url = self.base_url + resource_metadata['resource_path'] + path
            body = args[0]
            return _do_post(url, xwire.transport.json.serialize(body), return_type, cookies=get_cookies(self), headers=get_headers(self))

        return wrapper
    return decorator
