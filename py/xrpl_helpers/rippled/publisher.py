
import os
import time
from typing import Dict, Any, List  # noqa: F401
from xrpl_helpers.common.utils import read_json, write_json, read_txt
import json
import base64
import subprocess

from xrpl.core.binarycodec.main import decode

class PublisherClient(object):

    vl: Dict[str, Any] = {
        'public_key' : None,
        'manifest': None,
        'blob' : None,
        'signature' : None,
        'version' : 0
    }

    blob_json: Dict[str, Any] = {
        "sequence": 0,
        "expiration": 0,
        "validators": []
    }

    expiration: int = 86400 * 30 # expires in 30 days
    name: str = ''  # node1 | node2 | signer

    def __init__(cls, name: str) -> None:
        cls.name = name

        # os.makedirs('out', exist_ok=True)
        # try:
        #     cls.vl = read_json('out/vl.json')
        # except Exception as e:
        #     print(e)
        #     cls.vl = None

        # print(cls.vl)

        # if not cls.vl:
        #     print('RESETING - NO VL')
        #     cls.reset()
        #     return

        # if 'blob' not in cls.vl or cls.vl['blob'] == None:
        #     print('RESETING - NO BLOB')
        #     cls.reset()
        #     return

        # print(cls.vl)

        # print('READING...')
        # cls.blob_json = cls.decode_blob(cls.vl['blob'])
        # if not read_json(f'keystore/{cls.name}.json'):
        #     print('NO KEYS')
        #     cls.create_keys()
        #     cls.reset()

    def create_keys(cls) -> str:
        args1 = ['./validator-keys', 'create_keys', '--keyfile', f'keystore/{cls.name}/key.json']
        subprocess.call(args1)
        return read_json(f'keystore/{cls.name}/key.json')

    def set_domain(cls, domain: str) -> None:
        args1 = ['./validator-keys', 'set_domain', 'domain']
        subprocess.call(args1)

    def create_token(cls, domain: str) -> str:
        cls.set_domain(domain)
        out = open(f'keystore/{cls.name}/token.txt', 'w')
        args = ['./validator-keys', 'create_token', '--keyfile', f'keystore/{cls.name}/key.json']
        subprocess.call(args, stdout=out)
        return read_txt(f'keystore/{cls.name}/token.txt')

    def create_manifest(cls) -> str:
        out = open(f'keystore/{cls.name}/manifest.txt', 'w')
        args = ['./validator-keys', 'show_manifest', 'base64']
        subprocess.call(args, stdout=out)
        return read_txt(f'keystore/{cls.name}/manifest.txt')

    def get_signature(cls) -> str:
        out = open('out/signature.txt', 'w')
        args = ['/app/validator', 'sign', cls.encode_blob().hex()]
        subprocess.call(args, stdout=out)
        return read_txt('out/signature.txt')

    def export(cls) -> None:
        print('EXPORTING PUBLISHER LIST')
        manifest = [l.strip() for l in cls.get_manifest()]
        cls.vl['manifest'] = manifest[1]
        print(manifest)
        encoded = base64.b64decode(cls.vl['manifest']).hex()
        decoded: Dict[str, Any] = decode(encoded)
        cls.vl['public_key'] = decoded['PublicKey'].upper()

        cls.vl['blob'] = cls.encode_blob().decode('utf-8')
        signature = [l.strip() for l in cls.get_signature()]
        cls.vl['signature'] = signature[0]
        cls.vl['version'] = 1
        write_json(cls.vl, 'out/vl.json')

    def add_validator(cls, manifest: str):
        if not cls.vl:
            raise ValueError('INVALID VL')

        if not cls.blob_json:
            raise ValueError('INVALID BLOB JSON')

        print('ADDING MANIFEST TO VL')
        encoded = base64.b64decode(manifest).hex()
        decoded: Dict[str, Any] = decode(encoded)
        public_key: str = decoded['PublicKey'].upper()
        new_validator: Dict[str, Any] = {
            'validation_public_key': public_key,
            'manifest': manifest
        }
        vlist: List[Dict[str, Any]] = cls.blob_json['validators']
        vlist.append(new_validator)
        cls.blob_json['sequence'] += 1
        cls.blob_json['expiration'] = (int(time.time()) + cls.expiration) - 946684800
        # cls.blob_json['expiration'] = 721785600
        cls.blob_json['validators'] = vlist
        # print(cls.blob_json)
        cls.export()

    def remove_validator(cls, public_key: str):
        if not cls.vl:
            raise ValueError('INVALID VL')

        if not cls.blob_json:
            raise ValueError('INVALID BLOB JSON')

        vlist: List[Dict[str, Any]] = cls.blob_json['validators']
        cls.blob_json['sequence'] += 1
        cls.blob_json['expiration'] = (int(time.time()) + cls.expiration) - 946684800
        cls.blob_json['validators'] = [l for l in vlist if l['validation_public_key'] != public_key]
        cls.export()

    def encode_blob(cls) -> bytes:
        return base64.b64encode(json.dumps(cls.blob_json).encode("utf-8"))

    def decode_blob(cls, blob: str):
        return json.loads(base64.b64decode(blob))

    def decode_manifest(cls, manifest: str):
        encoded = base64.b64decode(manifest).hex()
        decoded: Dict[str, Any] = decode(encoded)
        return decoded

    def sign_unl(cls, manifests: List[str]):
        print(manifests)
        # encoded = base64.b64encode(manifest)
        # decoded: Dict[str, Any] = decode(encoded)
