#!/usr/bin/env python
# coding: utf-8
from typing import Dict, Any # noqa: F401

from core.rippled.utils import parse_rippled_features

result: Any = parse_rippled_features('/Users/dustedfloor/projects/transia-rnd/rippled-icv2/src/ripple/protocol/impl/Feature.cpp')
print(result)
