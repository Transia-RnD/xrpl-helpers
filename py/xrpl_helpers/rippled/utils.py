#!/usr/bin/env python
# coding: utf-8

import re
import os
import json
from datetime import datetime
from typing import Dict, Any, List  # noqa: F401

from xrpl_helpers.common.utils import read_json
import hashlib


def parse(value: str):
    if value == "no":
        return False
    else:
        return True


def parse_version_from_path(file_path):
    if "xahaud" in file_path:
        # Return the current year/month/day as the version
        return datetime.now().strftime('%Y.%m.%d')

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read all the lines
        lines = file.readlines()

    # Define the version string pattern
    pattern = r"versionString = \"([0-9a-zA-Z\.\-]+)\""

    # Iterate over each line
    for line in lines:
        # Search for the version pattern
        search = re.search(pattern, line)

        # If match is found
        if search:
            # Return the matched version
            if search.group(1) == "0.0.0":
                return datetime.now().strftime('%Y.%m.%d')

            return search.group(1)

    # If no version string found return None
    return None


def parse_rippled_amendments(path: str):
    with open(path, "r") as f:
        lines = f.readlines()
        amendments = {}
        for line in lines:
            if re.match(r"REGISTER_FEATURE", line) or re.match(r"REGISTER_FIX", line):
                amendment_name: str = ""
                if re.match(r"REGISTER_FIX", line):
                    amendment_name = (
                        re.search("REGISTER_FIX\)?.*?\((.*?),", line).group(1) or 0
                    )
                if re.match(r"REGISTER_FEATURE", line):
                    amendment_name = (
                        re.search("REGISTER_FEATURE\((.*?),", line).group(1) or 0
                    )
                supported = re.findall(r"Supported::(.*),", line)
                default_vote = re.findall(r"DefaultVote::(.*),", line)
                amendments[amendment_name] = {
                    "supported": parse(supported[0] if supported else "no"),
                    "default_vote": parse(default_vote[0] if default_vote else "no"),
                }
    return {
        k: hashlib.sha512(k.encode("utf-8")).digest().hex().upper()[:64]
        for (k, v) in amendments.items()
        if v["supported"] == True
    }

def convert_to_list_of_hashes(features):
    return list(features.values())

def update_amendments(features: Dict[str, Any]):
    # load the json string into a dictionary
    json_dict = read_json('genesis.json')

    new_amendments: List[str] = convert_to_list_of_hashes(features)

    # loop through the list of dictionaries in accountState
    for dct in json_dict['ledger']['accountState']:
        # check if the dictionary has a key called 'Amendments'
        if 'Amendments' in dct:
            # if it does, update it's value with the new amendments
            dct['Amendments'] = new_amendments

    return json_dict
