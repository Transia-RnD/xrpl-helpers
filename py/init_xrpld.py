#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any, List  # noqa: F401
import hashlib
import json
import base64

from xrpl_helpers.rippled.publisher import PublisherClient
from xrpl_helpers.rippled.validator import ValidatorClient

def generate_localnet_vl(domain: str, name: str, pv: int, v: int):

    for pvi in range(pv):
        index: int = pvi + 1
        validator = ValidatorClient(f'{name}_vmaster{index}')
        validator.create_keys()
        validator.create_token(f'{name}.master{index}.{domain}')
        validator.create_manifest()

    for vi in range(v):
        index: int = vi + 1
        validator = ValidatorClient(f'{name}_vnode{index}')
        validator.create_keys()
        validator.create_token(f'{name}.vnode{index}.{domain}')
        validator.create_manifest()

def generate_localnet_vl_manifests(name: str, pv: int, v: int) -> List[str]:
    manifests: List[str] = []
    for pvi in range(pv):
        index: int = pvi + 1
        validator = ValidatorClient(f'{name}_vmaster{index}')
        manifests.append(validator.read_manifest())

    for vi in range(v):
        index: int = vi + 1
        validator = ValidatorClient(f'{name}_vnode{index}')
        manifests.append(validator.read_manifest())
    return manifests

domain: str = 'transia.co'
name: str = 'mint'
private_validators: int = 1
validators: int = 1
# generate_localnet_vl(
#     domain,
#     name,
#     private_validators,
#     validators,
# )

# manifests: List[str] = generate_localnet_vl_manifests(
#     name,
#     private_validators,
#     validators,
# )
# print(manifests)
# publisher = PublisherClient(name)
# pk: str = 'CC9E8B118E8E927DA82A66B9D931E1AB6309BA32F057F8B216600B347C552006'
# manifest: str = 'JAAAAAFxIe101ANsZZGkvfnFTO+jm5lqXc5fhtEf2hh0SBzp1aHNwXMh7TN9+b62cZqTngaFYU5tbGpYHC8oYuI3G3vwj9OW2Z9gdkAnUjfY5zOEkhq31tU4338jcyUpVA5/VTsANFce7unDo+JeVoEhfuOb/Y8WA3Diu9XzuOD4U/ikfgf9SZOlOGcBcBJAw44PLjH+HUtEnwX45lIRmo0x5aINFMvZsBpE9QteSDBXKwYzLdnSW4e1bs21o+IILJIiIKU/+1Uxx0FRpQbMDA=='
# publisher.new(manifest)
# for m in manifests:
#     publisher.add_validator(m)
# publisher.sign_unl(0, 767784645)
