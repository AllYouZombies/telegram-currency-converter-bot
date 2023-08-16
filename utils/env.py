from typing import Any
from os import getenv as env


def get_env(key: str, default: Any = None) -> Any:
    """
    Get an environment variable and cast it to the correct type.
    :param key: environment variable name
    :param default: default value
    :return: environment variable value or default value
    """
    value = env(key, default)
    if value == '':
        return default
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    return value
