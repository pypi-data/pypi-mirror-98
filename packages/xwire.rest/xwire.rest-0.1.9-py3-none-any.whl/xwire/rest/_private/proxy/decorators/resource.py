from typing import TypeVar, Type
from xwire.common import decorator_utils

T = TypeVar('T')


def resource(resource_path: str):
    def decorator(cls: Type[T]) -> Type[T]:
        decorator_utils.set_decorator_metadata(cls, resource, {
            'resource_path': resource_path,
            'cookies': None,
            'headers': None
        })
        return cls
    return decorator

