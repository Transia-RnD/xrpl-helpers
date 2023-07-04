
import os
import time
from typing import Dict, Any, List  # noqa: F401
from xrpl_helpers.common.utils import read_json, write_json, read_txt
import json
import base64
import subprocess

from xrpl.core.binarycodec.main import decode

def encode_blob(blob: Dict[str, Any]) -> bytes:
    return base64.b64encode(json.dumps(blob).encode("utf-8"))

def decode_blob(blob: str):
    return json.loads(base64.b64decode(blob))

class Validator(object):
    pk: str = None
    manifest: str = None
    def __init__(self) -> None:
        pass

    @staticmethod
    def from_json(json: Dict[str, Any]):
        self = Validator()
        self.pk = json['validation_public_key']
        self.manifest = json['manifest']
        return self

    def to_dict(self):
        return {
            'validation_public_key': self.pk,
            'manifest': self.manifest,
        }


class Blob(object):
    sequence: int = None
    effective: str = None
    expiration: str = None
    validators: List[Validator] = []

    def __init__(self) -> None:
        pass

    @staticmethod
    def from_json(json: Dict[str, Any]):
        self = Blob()
        self.sequence = json['sequence']
        # self.effective = json['effective']
        self.expiration = json['expiration']
        self.validators = [Validator.from_json(v) for v in json['validators']]
        return self

    def to_dict(self):
        return {
            'sequence': self.sequence,
            'effective': self.effective,
            'expiration': self.expiration,
            'validators': [v.to_dict() for v in self.validators],
        }

class VL(object):
    public_key: str = None
    manifest: str = None
    blob: Blob = None
    signature: str = None
    version: int = None

    def __init__(self) -> None:
        pass

    @staticmethod
    def from_json(json: Dict[str, Any]):
        self = VL()
        # self.public_key = json['public_key']
        self.manifest = json['manifest']
        self.blob = Blob.from_json(decode_blob(json['blob']))
        self.signature = json['signature']
        self.version = json['version']
        return self

    def to_dict(self):
        return {
            'public_key': self.public_key,
            'manifest': self.manifest,
            'blob': encode_blob(self.blob.to_dict()).decode('utf-8'),
            'signature': self.signature,
            'version': self.version,
        }

class PublisherClient(object):

    name: str = ''
    key: Dict[str, Any] = {}
    vl: VL = None

    def __init__(cls, name: str) -> None:
        cls.name = name
        os.makedirs(f'keystore/{cls.name}_publisher', exist_ok=True)
        try:
            cls.key = read_json(f'keystore/{cls.name}_publisher/key.json')
            vl_dict: Dict[str, Any] = read_json(f'keystore/{cls.name}_publisher/vl.json')
            cls.vl = VL.from_json(vl_dict)
        except Exception as e:
            # print(e)
            cls.vl = None

        # print(cls.vl.to_dict())

    def new(cls, manifest: str):
        cls.vl = VL()
        cls.vl.manifest = manifest
        cls.vl.blob = Blob()
        cls.vl.blob.sequence = 1

    def add_validator(cls, manifest: str):
        if not cls.vl:
            raise ValueError('invalid vl')

        if not cls.vl.blob:
            raise ValueError('invalid blob')

        encoded = base64.b64decode(manifest).hex()
        decoded: Dict[str, Any] = decode(encoded)
        public_key: str = decoded['PublicKey'].upper()
        new_validator: Validator = Validator()
        new_validator.pk = public_key
        new_validator.manifest = manifest
        cls.vl.blob.validators.append(new_validator)

    def remove_validator(cls, public_key: str):
        if not cls.vl:
            raise ValueError('invalid vl')

        if not cls.blob_json:
            raise ValueError('invalid blob')

        vlist: List[Dict[str, Any]] = cls.blob_json['validators']
        cls.blob_json['sequence'] += 1
        cls.blob_json['expiration'] = (int(time.time()) + cls.expiration) - 946684800
        cls.blob_json['validators'] = [l for l in vlist if l['validation_public_key'] != public_key]

    def sign_unl(
            cls,
            effective: int,
            expiration: int
        ):
        if not cls.vl:
            raise ValueError('invalid vl')

        if len(cls.vl.blob.validators) == 0:
            raise ValueError('must have at least 1 validator')

        vl_path = f'keystore/{cls.name}_publisher/vl.json'
        out = open(vl_path, 'w')
        vl_manifests: List[str] = [v.manifest for v in cls.vl.blob.validators]
        args = [
            '../bin/validator-list',
            'sign',
            '--private_key', cls.key['privateKey'],
            '--sequence', str(cls.vl.blob.sequence),
            '--expiration', str(expiration),
            '--manifest', cls.key['manifest'],
            '--manifests', ','.join(vl_manifests),
        ]
        subprocess.call(args, stdout=out)
        return read_txt(vl_path)
