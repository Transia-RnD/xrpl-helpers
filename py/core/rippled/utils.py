#!/usr/bin/env python
# coding: utf-8

import re
from typing import Dict, Any # noqa: F401

from core.common.utils import read_file


def parse(value: str):
    if value == 'no':
        return False
    else:
        return True

def parse_rippled_features(path: str):
    with open(path, 'r') as f:
        lines = f.readlines()
        features = {}
        for line in lines:
            if re.match(r'REGISTER_FEATURE', line) or re.match(r'REGISTER_FIX', line):
                feature_name: str = ''
                if re.match(r'REGISTER_FIX', line):
                    feature_name = re.search('REGISTER_FIX\)?.*?\((.*?),', line).group(1) or 0
                if re.match(r'REGISTER_FEATURE', line):
                    feature_name = re.search('REGISTER_FEATURE\((.*?),', line).group(1) or 0
                supported = re.findall(r'Supported::(.*),', line)
                default_vote = re.findall(r'DefaultVote::(.*),', line)
                features[feature_name] = {
                    'supported': parse(supported[0] if supported else 'no'),
                    'default_vote': parse(default_vote[0] if default_vote else 'no')
                }
    print([k for k, v in features.items() if v['supported'] == True])
    return [k for k, v in features.items() if v['supported'] == True]
