#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any  # noqa: F401
import hashlib
import json
import base64

# k = 'Import'
# print(hashlib.sha512(k.encode("utf-8")).digest().hex().upper()[:64])

from xrpl_helpers.rippled.validator import ValidatorClient

# token: str = '''
# eyJtYW5pZmVzdCI6IkpBQUFBQVJ4SWUyNlROZGV2SldXQmxJRE1ZQVRBVW9pRisrRURlaGRa
# T1MvcWVFdTNxYjMvbk1oQXkzd3FPaDBhOTVTUm9WMzVlcXVWaE9lZnA5cGlSUjdiMHRWVW4w
# TjNHMm5ka1l3UkFJZ1U5cnNmbkIzZWUxWm5SSEdHUmRGZm5iU00zTkJsdzZTSk02dE00d0xs
# VmNDSUI2N041cHo1Y3VlQVZQbVpvMHhodzJsMkNjUk56RXpWbXFKc1k3NkNYbXhjQkpBYVVu
# ZUh4S015Yi8wVG1LUDM1MFdneEtIVjB2aWUxN2tKRmdUVHVmUDNaa2p2SVI5NmRIcUlDekNu
# R1Y2aktSTGJONWNsWFRsUHR3Wld5anU3WEtwQkE9PSIsInZhbGlkYXRpb25fc2VjcmV0X2tl
# eSI6IkNDRkNCNUZGQjYyNDczQzVBQkQ1QTdERDhFRjdGNzA3MEM1ODIwQTc0MDlGNDY4NEQx
# NkFFQTVENEFCNDk2MEQifQ==
# '''
# token_json = json.loads(base64.b64decode(token))
# print(json.dumps(token_json, indent=4, sort_keys=True))
# print(token_json['validation_secret_key'])
# manifest_json = base64.b64decode(token_json['manifest']).hex()
# print(manifest_json)

# publisher = ValidationPublisher('publisher', 'node1')
# # print(publisher)
# print(json.dumps(publisher.vl, indent=4, sort_keys=True))
# print(json.dumps(publisher.blob_json, indent=4, sort_keys=True))
# print(publisher.reset())

# 1. Create Burn Master (The master node)
# publisher = ValidatorClient('burn_vmaster')
# publisher.create_keys()
# publisher.create_token('burn.master.transia.co')
# publisher.create_manifest()

# 2. Create Burn Node1 (The peer node)
# publisher = ValidatorClient('burn_vnode1')
# publisher.create_keys()
# publisher.create_token('burn.node1.transia.co')
# publisher.create_manifest()

# 3. Create Burn node2 (The peer node)
# publisher = ValidatorClient('burn_vnode2')
# publisher.get_or_create_keys()
# publisher.create_token('burn.node2.transia.co')
# publisher.create_manifest()

# manifest: str = """
# JAAAAAFxIe15tDJnJdSr9uS3nL945/83I4UV7IbtAPYhfUcM405tiHMh7bLZujYK907eoOADwK6XYxc+VBZTy90vN5zgJVoW9dUEdkAarPTP2tRmQHpWzbMbVhkNKWDYBWnoXJwnaz8av50WG6p/ISkm6nuJi0AajSc7UJ/ttANSGwYqQuuhFGcyrfUGcBJAOzvuJnZfQ5NUGzBjczX/A1C3mDQAA4CCsDXIso2voN9voxSHxbKBUAGcsexdEpRW2nK2tziUJI3Eye3XbDzfBg==
# """
# publisher = ValidationPublisher('publisher', 'vmaster')
# blob = publisher.decode_manifest(manifest)
# print(blob)
