#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any  # noqa: F401
import json
import yaml


def read_txt(path: str) -> Dict[str, object]:
    """
    Reads txt from file path
    :return: Dict[str, object]
    """
    with open(path) as json_file:
        return json_file.readlines()


def read_file(path: str) -> str:
    """Read File

     # noqa: E501

    :param path: Path to file
    :type path: str

    :rtype: str
    """
    with open(path, 'r') as f:
        return f.read()


def write_file(path: str, data: Any) -> str:
    """Write File

     # noqa: E501

    :param path: Path to file
    :type path: str

    :rtype: str
    """
    with open(path, "w") as f:
        return f.write(data)


def read_json(path: str) -> Dict[str, object]:
    """Read Json

     # noqa: E501

    :param path: Path to json
    :type path: str

    :rtype: Dict[str, object]
    """
    with open(path) as json_file:
        return json.load(json_file)


def write_json(path: str, data: Dict[str, object]):
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
