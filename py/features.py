#!/usr/bin/env python
# coding: utf-8
# poetry run python3 features.py /Users/dustedfloor/projects/transia-rnd/rippled-icv2/src/ripple/protocol/Feature.h dangell7/vala/1/features.json

from typing import Dict, Any, List # noqa: F401
import sys
import json

from google.cloud import storage

from core.common.utils import write_json
from core.rippled.utils import parse_rippled_features

def save_features(features: Dict[str, Any], dest_file):
    # write_json(features, dst_file)
    bucket = storage.Client().get_bucket('thehub-builds')
    blob = bucket.blob(dest_file)
    blob.upload_from_string(json.dumps(features), 'application/json')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 features.py <source file> <dest file>")
        sys.exit()

    src_file: str = sys.argv[1]
    dst_file: str = sys.argv[2]
    if src_file[-1] == '/':
        print("Path Usage: app/src/ripple - no forwardslash")
        sys.exit()

    features: Any = parse_rippled_features(src_file)
    save_features(features, dst_file)
