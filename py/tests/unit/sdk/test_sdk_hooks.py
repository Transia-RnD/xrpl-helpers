#!/usr/bin/env python
# coding: utf-8

# import json
import logging
from typing import Dict, Any, List  # noqa: F401

import binascii

from testing_config import BaseTestConfig
from xrpl_helpers.sdk.hooks import (
    calculate_hook_on,
    hex_namespace,
    hex_hook_parameters
)

# -----------------------------------------------------------------------------

logger = logging.getLogger('app')


class TestXrplHooks(BaseTestConfig):

    def test_binary(cls):
        CONTRACT_PATH = './tests/fixtures/starter.c.wasm'
        with open(CONTRACT_PATH, 'rb') as f:
            content = f.read()
        binary = binascii.hexlify(content).decode('utf-8').upper()
        print(binary)
        expected: str = "0061736D01000000011C0460057F7F7F7F7F017E60037F7F7E017E60027F7F017F60017F017E02230303656E76057472616365000003656E7606616363657074000103656E76025F670002030201030503010002062B077F0141B088040B7F004180080B7F0041A6080B7F004180080B7F0041B088040B7F0041000B7F0041010B07080104686F6F6B00030AC4800001C0800001017F230041106B220124002001200036020C41920841134180084112410010001A410022002000420010011A41012200200010021A200141106A240042000B0B2C01004180080B254163636570742E633A2043616C6C65642E00224163636570742E633A2043616C6C65642E22"
        cls.assertEqual(
            binary,
            expected
        )

    def test_calculate_hook_on_all(cls):
        hook_on: str = calculate_hook_on([])
        cls.assertEqual(
            hook_on,
            '000000000000000000000000000000000000000000000000000000003e3ff5bf'
        )

    def test_calculate_hook_on_account_set(cls):
        invoke_on: List[str] = ['ttACCOUNT_SET']
        hook_on_values: List[str] = [v for v in invoke_on]
        hook_on: str = calculate_hook_on(hook_on_values)
        cls.assertEqual(
            hook_on,
            '000000000000000000000000000000000000000000000000000000003e3ff5b7'
        )

    def test_hook_namespace(cls):
        namespace: str = 'starter'
        sha_namespace: str = hex_namespace(namespace)
        cls.assertEqual(
            sha_namespace,
            '4FF9961269BF7630D32E15276569C94470174A5DA79FA567C0F62251AA9A36B9'
        )

    def test_hook_parameters(cls):
        parameters: List[Any] = [{
            'HookParameter': {
                'HookParameterName': 'name1',
                'HookParameterValue': 'value1',
            }
        }]
        result: str = hex_hook_parameters(parameters)
        cls.assertEqual(
            result,
            [
                {'HookParameter': {
                    'HookParameterName': '6E616D6531',
                    'HookParameterValue': 'value1'
                }}
            ]
        )
