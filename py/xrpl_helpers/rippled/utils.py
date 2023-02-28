#!/usr/bin/env python
# coding: utf-8

import re
from typing import Dict, Any  # noqa: F401

from xrpl_helpers.common.utils import read_file
import hashlib


def parse(value: str):
    if value == "no":
        return False
    else:
        return True


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
