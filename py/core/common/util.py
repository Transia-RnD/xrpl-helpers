#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any # noqa: F401
import json
import yaml


def read_file(path: str) -> str:
    """Read File

     # noqa: E501

    :param path: Path to file
    :type path: str

    :rtype: str
    """
    with open(path, 'r') as f:
        return f.read()


def read_json(path: str) -> Dict[str, object]:
    """Read Json

     # noqa: E501

    :param path: Path to json
    :type path: str

    :rtype: Dict[str, object]
    """
    with open(path) as json_file:
        return json.load(json_file)


def write_json(data: Dict[str, object], path: str):
    """Write Json

     # noqa: E501

    :param path: Path to json
    :type path: str

    :rtype: None
    """
    with open(path, 'w') as json_file:
        json.dump(data, json_file)
    return True


def read_yaml(path: str) -> Dict[str, object]:
    """Read Yaml

     # noqa: E501

    :param path: Path to json
    :type path: str

    :rtype: Dict[str, object]
    """
    with open(path) as yaml_file:
        return yaml.safe_load(yaml_file)


