#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Package Utilities Module

"""
import logging
import logging.config
import functools
import operator
from pathlib import Path
import time
from typing import Any, Dict, List, Optional, Union

from saw.pkg_globals import FONT_SIZE, TIME_FORMAT


def docker_secret(secret_name: str) -> Optional[str]:
    """
    Read Docker secret file.

    Args:
        secret_name: name of secret

    Returns:
        secret value or None if not found
    """
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as f:
            return f.read().strip('\n')
    except IOError:
        return None


def logger_setup(file_path: Union[None, Path, str] = None,
                 logger_name: str = 'package') -> logging.Logger:
    """
    Configure logger with console and file handlers.

    Args:
        file_path: path to log file
        logger_name: name of logger

    Returns:
        logging.Logger: configured logger
    """
    if file_path:
        file_path = (Path(file_path).absolute()
                     if isinstance(file_path, str) else file_path.absolute())
        file_path = (timestamp_dir(file_path.parent,
                                   file_path.name).with_suffix('.log'))
    else:
        file_path = 'info.log'
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': ('%(levelname)s - %(name)s -> Line: %(lineno)d <- '
                           '%(message)s'),
            },
            'file': {
                'format': ('%(asctime)s - %(levelname)s - %(module)s.py -> '
                           'Line: %(lineno)d <- %(message)s'),
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'WARNING',
                'formatter': 'console',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'encoding': 'utf8',
                'level': 'DEBUG',
                'filename': file_path,
                'formatter': 'file',
                'mode': 'w',
            },
        },
        'loggers': {
            'package': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
    logging.config.dictConfig(config)
    return logging.getLogger(logger_name)


def nested_get(nested_dict: Dict[Any, Any], key_path: List[Any]) -> Any:
    """
    Retrieve value from a nested dictionary.

    Args:
        nested_dict: nested dictionary
        key_path: list of key levels with the final entry being the target

    Returns:
        Any: target value
    """
    return functools.reduce(operator.getitem, key_path, nested_dict)


def nested_set(nested_dict: Dict[Any, Any], key_path: List[Any], value: Any):
    """
    Set object of nested dictionary.

    Args:
        nested_dict: nested dictionary
        key_path: list of key levels with the final entry being the target
        value: target value

    Returns:
        Any: target value
    """
    nested_get(nested_dict, key_path[:-1])[key_path[-1]] = value


def timestamp_dir(base_dir: Path, desc: Optional[str] = None):
    """
    Generate path to new directory with a timestamp.

    Args:
        base_dir: base directory
        desc: description of directory

    Returns:
        Path: path to new directory
    """
    desc = '' if desc is None else f'{desc}-'
    return base_dir / time.strftime(f'{desc}{TIME_FORMAT}')


if __name__ == '__main__':
    pass
