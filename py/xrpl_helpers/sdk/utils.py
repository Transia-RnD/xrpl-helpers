#!/usr/bin/env python
# coding: utf-8

# import json
from typing import Dict, Any  # noqa: F401

import binascii
import json
from symtable import Symbol
from typing import Any, Dict, List

from xrpl.models.transactions import Memo


def symbol_to_hex(symbol):
    """symbol_to_hex."""
    if len(symbol) > 3:
        bytes_string = bytes(str(symbol).encode("utf-8"))
        return bytes_string.hex().upper().ljust(40, "0")
    return symbol


def hex_to_symbol(hex):
    """hex_to_symbol."""
    if len(hex) > 3:
        return bytes.fromhex(str(hex)).decode("utf-8")
    return hex


def hex_encode_decode(value: str):
    binascii.hexlify(value.encode("utf8")).decode("utf-8").upper()


def hex_decode(value: bytes):
    binascii.unhexlify(value).decode("utf-8")


def create_memo(data: str, format: str, type: str):
    result = Memo(
        memo_data=hex_encode_decode(data),
        memo_format=hex_encode_decode(format),
        memo_type=hex_encode_decode(type),
    )
    return result


def read_memo(memo: Memo):
    result = {
        "memo_data": hex_decode(memo.memo_data),
        "memo_format": hex_decode(memo.memo_format),
        "memo_type": hex_decode(memo.memo_type),
    }
    return result


# memos: [{'data': object, 'format': xls43-/message, 'type': xls-42/signature}]
def create_memos(memos: List[Dict[str, Any]]):
    hex_memos = []
    for memo in memos:
        hex_memos.append(
            create_memo(json.dumps(memo["data"]), memo["format"], memo["type"])
        )
    return hex_memos


# memos: [{'data': hex, 'format': hex, 'type': hex}]
def read_memos(memos: List[Memo]):
    hex_memos = []
    for memo in memos:
        hex_memos.append(read_memo(memo))
    return hex_memos


# types: List[str] = ['Escrow', 'PaymentChannel', 'URIToken']
def get_object_id(meta: Dict[str, Any], type: str) -> str:
    created_list = [node for node in meta['AffectedNodes'] if 'CreatedNode' in node and node['CreatedNode']['LedgerEntryType'] == type]
    if len(created_list) > 0:
        return created_list[0]['CreatedNode']['LedgerIndex']
    return None
