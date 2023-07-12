#!/usr/bin/env python
# coding: utf-8

from xrpl_helpers.common.utils import read_json, write_json, write_file
from typing import Dict, Any, List  # noqa: F401

amendments = read_json('amendments/features.json')

amendment_list: List[str] = []
cfg_list: str = ''
for k, v in amendments.items():
    amendment_list.append(v)
    cfg_list += f'{v} {k}'
    cfg_list += "\n"

write_json('amendments/genesis.json', amendment_list)
write_file('amendments/cfg.txt', cfg_list)
