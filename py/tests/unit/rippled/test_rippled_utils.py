#!/usr/bin/env python
# coding: utf-8

import json
import logging
from typing import Dict, Any, List  # noqa: F401

# -----------------------------------------------------------------------------

from testing_config import BaseTestConfig
from xrpl_helpers.rippled.utils import (
    parse_rippled_features,
)

logger = logging.getLogger('app')


class TestRippledUtils(BaseTestConfig):

    feature_list: List[str] = [
        'Flow',
        'FlowCross',
        'CryptoConditionsSuite',
        'fix1513',
        'DepositAuth'
    ]

    def test_parse_rippled_features(cls):
        result: Any = parse_rippled_features('./tests/fixtures/core.h')
        cls.assertEqual(result, cls.feature_list)
