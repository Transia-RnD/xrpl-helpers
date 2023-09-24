#!/usr/bin/env python
# coding: utf-8
# poetry run python3 release.py dangell7 vala linux/amd /Users/denisangell/projects/xrpl-labs/rippled

from typing import Dict, Any, List  # noqa: F401
import sys
import json

from xrpl_helpers.libs.google.storage import GCPStorageClient

from xrpl_helpers.common.utils import write_json
from xrpl_helpers.rippled.utils import parse_rippled_amendments, parse_version_from_path

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python3 release.py <namespace> <buildname> <platform> <source file>"
        )
        sys.exit()

    namespace: str = sys.argv[1]
    build_name: str = sys.argv[2]
    platform: str = sys.argv[3]
    rippled_dir: str = sys.argv[4]
    if rippled_dir[-1] == "/":
        print("Path Usage: app/src/ripple - no forwardslash")
        sys.exit()

    try:
        build_path: str = f"{namespace}/{build_name}/"
        client: GCPStorageClient = GCPStorageClient(
            project_id="thelab-924f3", bucket_name="thelab-builds"
        )

        # get Version
        version_file: str = rippled_dir + "/src/ripple/protocol/impl/BuildInfo.cpp"
        version_str: str = parse_version_from_path(version_file)

        # get features list
        features_file: str = rippled_dir + "/src/ripple/protocol/impl/Feature.cpp"
        features_blob: str = build_path + f"{version_str}" + "/features.json"
        features: Any = parse_rippled_amendments(features_file)

        # save features list - gcs
        client.upload(blob_name=features_blob, payload=features)

        # save feature list - local
        # write_json('amendments/features.json', features)
    except Exception as e:
        print(e)
