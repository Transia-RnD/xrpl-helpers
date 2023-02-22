#!/usr/bin/env python
# coding: utf-8

# import json
from typing import List, Dict, Any, Optional  # noqa: F401

import hashlib
import binascii


def calculate_hook_on(arr: list) -> str:
    """
    Calculate the hook on value for a given list of transaction types.

    :param arr: List of transaction types
    :return: The hook on value
    """
    tts = {
        'ttPAYMENT': 0,
        'ttESCROW_CREATE': 1,
        'ttESCROW_FINISH': 2,
        'ttACCOUNT_SET': 3,
        'ttESCROW_CANCEL': 4,
        'ttREGULAR_KEY_SET': 5,
        'ttOFFER_CREATE': 7,
        'ttOFFER_CANCEL': 8,
        'ttTICKET_CREATE': 10,
        'ttSIGNER_LIST_SET': 12,
        'ttPAYCHAN_CREATE': 13,
        'ttPAYCHAN_FUND': 14,
        'ttPAYCHAN_CLAIM': 15,
        'ttCHECK_CREATE': 16,
        'ttCHECK_CASH': 17,
        'ttCHECK_CANCEL': 18,
        'ttDEPOSIT_PREAUTH': 19,
        'ttTRUST_SET': 20,
        'ttACCOUNT_DELETE': 21,
        'ttHOOK_SET': 22,
        'ttNFTOKEN_MINT': 25,
        'ttNFTOKEN_BURN': 26,
        'ttNFTOKEN_CREATE_OFFER': 27,
        'ttNFTOKEN_CANCEL_OFFER': 28,
        'ttNFTOKEN_ACCEPT_OFFER': 29
    }

    s = '0x3e3ff5bf'
    for n in arr:
        v = int(s, 16)
        v ^= 1 << tts[n]
        s = "0x" + hex(v)[2:]

    s = s.replace('0x', '')
    s = s.zfill(64)
    return s


def hex_namespace(namespace: str) -> str:
    """
    Hash the encoded namespace and return the hex upper
    """
    return hashlib.sha256(namespace.encode('utf-8')).digest().hex().upper()


def hex_hook_parameters(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    This function takes a dictionary and returns a list.
    """
    hook_parameters: List[Dict[str, Any]] = []
    for parameter in data:
        hook_parameters.append({
            'HookParameter': {
                'HookParameterName': binascii.hexlify(
                    parameter['HookParameter']['HookParameterName'].encode('utf8')
                ).decode('utf-8').upper(),
                'HookParameterValue': parameter['HookParameter']['HookParameterValue']
            }
        })
    return hook_parameters
