#!/usr/bin/env python
# coding: utf-8

from xrpl_helpers.rippled.utils import parse_version_from_path

rippled_dir: str = "/Users/denisangell/projects/xrpl-labs/xahaud"
features_file: str = rippled_dir + "/src/ripple/protocol/impl/BuildInfo.cpp"
version_str: str = parse_version_from_path(features_file)
print(version_str)
