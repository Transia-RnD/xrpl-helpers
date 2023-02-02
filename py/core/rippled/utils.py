#!/usr/bin/env python
# coding: utf-8

import re
from typing import Dict, Any # noqa: F401

from core.common.utils import read_file


def parse_rippled_features(path: str):
    result = read_file(path)
    # find all the extern uint256 const variables
    pattern = r'extern uint256 const (\w+);'
    matches = re.findall(pattern, result)

    # return the list of variables
    return matches
