import typing

import dataclasses
import logging
import os
import sys

from typing import Any, Dict, Tuple, Union

from polyswarmdconfig.exceptions import MissingConfigValueError


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Config:
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'Config':
        try:
            return cls(**cls.populate(config))
        except TypeError as e:
            logger.exception('Missing value while populating %s', cls.__name__)
            raise MissingConfigValueError from e

    @classmethod
    def from_dict_and_environment(cls, config: Dict[str, Any]) -> 'Config':
        cls.overlay_environment(config)
        try:
            return cls(**cls.populate(config))
        except TypeError as e:
            logger.exception('Missing value while populating %s', cls.__name__)
            raise MissingConfigValueError from e

    @classmethod
    def populate(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        module = sys.modules[cls.__module__]
        return {k: cls.get_value(k, v, module) for k, v in config.items() if typing.get_type_hints(cls).get(k)}

    @classmethod
    def get_value(cls, key, value, module):
        if not isinstance(value, dict):
            return cls.correct_type(key, value)
        elif module and hasattr(module, key.capitalize()):
            sub_config_class = getattr(module, key.capitalize())
            if issubclass(sub_config_class, Config):
                sub_config = sub_config_class.from_dict(value)
                return sub_config

    @classmethod
    def correct_type(cls, key: str, value: Any) -> Any:
        cast = typing.get_type_hints(cls).get(key)
        if cast and cast in [int, str]:
            return cast(value)
        elif cast and cast in [bool]:
            return cls._attempt_to_extract_bool(value)
        elif cast and cast in [list]:
            return cls._attempt_to_extract_list(value)
        else:
            return value

    @classmethod
    def overlay_environment(cls, config: Dict[str, Any]):
        name = cls.__name__.upper()
        for key, value in os.environ.items():
            if key.startswith(name):
                cls.overlay_matching_value(key.replace(f'{name}_', ''), value, config)

    @classmethod
    def overlay_matching_value(cls, key: str, value: Union[str, int, bytes], config: Dict[str, Any]):
        module = sys.modules[cls.__module__]
        current = config
        rest = key
        while True:
            title, rest = Config.split(rest)
            if module and hasattr(module, title.capitalize()):
                module = sys.modules[getattr(module, title.capitalize()).__module__]
                found_value = current.get(title.lower())
                if found_value and isinstance(found_value, dict):
                    current = found_value
                else:
                    current[title] = {}
                    current = current[title]
            else:
                # Not a sub config, just store the value
                current['_'.join([title, rest.lower()]) if rest else title] = value
                break

    @staticmethod
    def split(key: str) -> Tuple[str, str]:
        separated = key.split('_', 1)
        title = separated[0].lower()
        rest = separated[1] if len(separated) > 1 else ''
        return title, rest

    @staticmethod
    def _attempt_to_extract_bool(value):
        if isinstance(value, str):
            return value.lower() not in ('false', '0', '')
        else:
            return bool(value)

    @staticmethod
    def _attempt_to_extract_list(value):
        items_delimiter = ','
        return list(map(str.strip, value.split(items_delimiter)))
