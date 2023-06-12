#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any, List  # noqa: F401
from xrpl_helpers.common.utils import read_json, read_txt
import subprocess

from xrpl.core.binarycodec.main import decode

class ValidatorClient(object):

    expiration: int = 86400 * 30 # expires in 30 days
    name: str = ''  # node1 | node2 | signer

    def __init__(cls, name: str) -> None:
        cls.name = name

    def create_keys(cls) -> str:
        args1 = ['./validator-keys', 'create_keys', '--keyfile', f'keystore/{cls.name}/key.json']
        subprocess.call(args1)
        return read_json(f'keystore/{cls.name}/key.json')

    def set_domain(cls, domain: str) -> None:
        args1 = ['./validator-keys', 'set_domain', domain]
        subprocess.call(args1)

    def create_token(cls, domain: str) -> str:
        # cls.set_domain(domain)
        out = open(f'keystore/{cls.name}/token.txt', 'w')
        args = ['./validator-keys', 'create_token', '--keyfile', f'keystore/{cls.name}/key.json']
        subprocess.call(args, stdout=out)
        return read_txt(f'keystore/{cls.name}/token.txt')

    def create_manifest(cls) -> str:
        out = open(f'keystore/{cls.name}/manifest.txt', 'w')
        args = ['./validator-keys', 'show_manifest', 'base64', '--keyfile', f'keystore/{cls.name}/key.json']
        subprocess.call(args, stdout=out)
        return read_txt(f'keystore/{cls.name}/manifest.txt')
