from typing import TypeVar, Dict, Any

from xwire.common import decorator_utils

from xwire.transport._private.decorators import serializable
from xwire.transport._private.exceptions import SerializationError


T = TypeVar('T')


def serialize(data: T, **kwargs) -> Dict[str, Any]:
    if not decorator_utils.has_decorator(data, serializable):
        raise SerializationError('Object must be decorated with @xwire.serializable in order to be serialized')
    else:
        metadata = decorator_utils.get_decorator_metadata(data, serializable)
        serialized = {}
        for k, v in metadata['fields'].items():
            if isinstance(v, list) and len(v) > 0 and decorator_utils.has_decorator(v[0], serializable):
                serialized[k] = [serialize(item) for item in v]
            elif decorator_utils.has_decorator(v, serializable):
                serialized[k] = serialize(v)
            else:
                serialized[k] = v

        return serialized
