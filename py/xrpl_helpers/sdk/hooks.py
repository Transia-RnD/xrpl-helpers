#!/usr/bin/env python
# coding: utf-8

# import json
from typing import List, Dict, Any, Optional  # noqa: F401

# -----------------------------------------------------------------------------

import hashlib
import binascii

from xrpl.core.binarycodec.definitions import (
    _TRANSACTION_TYPE_MAP,
    _TRANSACTION_TYPES
)


def calculate_hook_on(arr: list) -> str:
    """
    Calculate the hook on value for a given list of transaction types.

    :param arr: List of transaction types
    :return: The hook on value
    """
    tts = _TRANSACTION_TYPE_MAP
    s = "0x3e3ff5bf"
    for n in arr:
        if n not in _TRANSACTION_TYPES:
            raise KeyError("invalid transaction type array")
        v = int(s, 16)
        v ^= 1 << tts[n]
        s = "0x" + hex(v)[2:]
    s = s.replace("0x", "")
    s = s.zfill(64)
    return s.upper()


def hex_namespace(namespace: str) -> str:
    """
    Hash the encoded namespace and return the hex upper
    """
    return hashlib.sha256(namespace.encode("utf-8")).digest().hex().upper()


def hex_hook_parameters(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    This function takes a dictionary and returns a list.
    """
    hook_parameters: List[Dict[str, Any]] = []
    for parameter in data:
        hook_parameters.append(
            {
                "HookParameter": {
                    "HookParameterName": binascii.hexlify(
                        parameter["HookParameter"]["HookParameterName"].encode("utf8")
                    )
                    .decode("utf-8")
                    .upper(),
                    "HookParameterValue": binascii.hexlify(
                        parameter["HookParameter"]["HookParameterValue"].encode("utf8")
                    )
                    .decode("utf-8")
                    .upper(),
                }
            }
        )
    return hook_parameters
