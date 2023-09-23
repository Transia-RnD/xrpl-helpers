#!/usr/bin/env python
# coding: utf-8
# poetry run python3 version.py dangell7 vala linux/amd /Users/denisangell/projects/xrpl-labs/rippled

from typing import Dict, Any, List  # noqa: F401
import sys
import json

from xrpl_helpers.libs.google.storage import GCPStorageClient

from xrpl_helpers.common.utils import write_file
from xrpl_helpers.rippled.utils import parse_version_from_path

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python3 version.py <namespace> <buildname> <platform> <source file> <dest file>"
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

        # get version
        version_file: str = rippled_dir + "/src/ripple/protocol/impl/BuildInfo.cpp"
        version_str: str = parse_version_from_path(version_file)

        # save version - gcs
        version_blob: str = build_path + f"{version_str}" + "/version.txt"
        client.upload(blob_name=version_blob, payload=version_str)

        # save version - local
        # write_file('amendments/version.txt', version_str)
    except Exception as e:
        print(e)
