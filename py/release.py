#!/usr/bin/env python
# coding: utf-8
# poetry run python3 release.py dangell7 vala 1 linux/amd /Users/dustedfloor/projects/xrpl-labs/rippled-sandbox

from typing import Dict, Any, List  # noqa: F401
import sys
import json

from xrpl_helpers.libs.google.storage import GCPStorageClient

from xrpl_helpers.common.utils import write_json
from xrpl_helpers.rippled.utils import parse_rippled_amendments

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: python3 release.py <namespace> <buildname> <version> <platform> <source file> <dest file>"
        )
        sys.exit()

    namespace: str = sys.argv[1]
    build_name: str = sys.argv[2]
    version: str = sys.argv[3]
    platform: str = sys.argv[4]
    rippled_dir: str = sys.argv[5]
    if rippled_dir[-1] == "/":
        print("Path Usage: app/src/ripple - no forwardslash")
        sys.exit()

    try:
        build_path: str = f"{namespace}/{build_name}/{version}"
        client: GCPStorageClient = GCPStorageClient(
            project_id="thelab-924f3", bucket_name="thelab-builds"
        )

        # save features list
        features_file: str = rippled_dir + "/src/ripple/protocol/impl/Feature.cpp"
        features_blob: str = build_path + "/features.json"
        features: Any = parse_rippled_amendments(features_file)
        client.upload(blob_name=features_blob, payload=features)

        # # save rippled
        # rippled_file: str = rippled_dir + "/.build/rippled"
        # rippled_blob: str = build_path + f"/rippled-{platform}"
        # client.upload(blob_name=rippled_blob, file=rippled_file)
    except Exception as e:
        print(e)
