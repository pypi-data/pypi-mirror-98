import re
import logging

from dataclasses import fields
from typing import TypeVar, Type, Dict, Any, get_origin, get_args

from xwire.common import decorator_utils

from xwire.transport._private.decorators import serializable
from xwire.transport._private.exceptions import DeserializationError

logger = logging.getLogger(__name__)

T = TypeVar('T')

_snake_case_regex = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


def _snake_case(s: str) -> str:
    return _snake_case_regex.sub(r'_\1', s).lower()


def deserialize(json: Dict[str, Any], target: Type[T]) -> T:
    if not decorator_utils.has_decorator(target, serializable):
        raise DeserializationError('Target must be decorated with @xwire.serializable in order to be deserialized to')
    else:
        try:
            snake_case_json = {_snake_case(k): v for k, v in json.items()}
            deserialized = {}
            for field in fields(target):
                if field.name not in snake_case_json:
                    logger.debug(f'Error while parsing JSON: {str(json)}')
                    raise DeserializationError(f'Missing required field in json "{field.name}"')
                json_value = snake_case_json[field.name]
                if get_origin(field.type) is list and decorator_utils.has_decorator(get_args(field.type)[0], serializable):
                    if not isinstance(json_value, list):
                        raise DeserializationError(f'Field "{field.name}" is of type {field.type} on target schema, but incoming json value is not a list: "{json_value}"')
                    deserialized[field.name] = [deserialize(item, get_args(field.type)[0]) for item in json_value]
                elif get_origin(field.type) is dict and decorator_utils.has_decorator(get_args(field.type)[1], serializable):
                    if not isinstance(json_value, dict):
                        raise DeserializationError(f'Field "{field.name}" is of type {field.type} on target schema, but incoming json value is not a dict: "{json_value}"')
                    deserialized[field.name] = {k: deserialize(v, get_args(field.type)[1]) for k, v in json_value.items()}
                elif decorator_utils.has_decorator(field.type, serializable):
                    if not isinstance(json_value, dict):
                        raise DeserializationError(f'Field "{field.name}" is of type {field.type} on target schema, but incoming json value is not an object: "{json_value}"')
                    deserialized[field.name] = deserialize(json_value, field.type)
                else:
                    deserialized[field.name] = json_value
        except DeserializationError as e:
            raise e
        except Exception as e:
            logger.debug(f'Error while parsing JSON: {str(json)}')
            raise DeserializationError(f'Unexpected deserialization error: {e}')
        else:
            return target(**deserialized)
