#!/usr/bin/env python
# coding: utf-8

import json
import logging
from typing import Dict, Any, List  # noqa: F401

# -----------------------------------------------------------------------------

from testing_config import BaseTestConfig
from xrpl_helpers.rippled.utils import (
    parse_rippled_amendments,
)

logger = logging.getLogger("app")


class TestRippledUtils(BaseTestConfig):
    amendment_list: Dict[str, str] = {
        "Flow": "740352F2412A9909880C23A559FCECEDA3BE2126FED62FC7660D628A06927F11",
        "FlowCross": "3012E8230864E95A58C60FD61430D7E1B4D3353195F2981DC12B0C7C0950FFAC",
        "CryptoConditionsSuite": "86E83A7D2ECE3AD5FA87AB2195AE015C950469ABF0B72EAACED318F74886AE90",
        "fix1513": "67A34F2CF55BFC0F93AACD5B281413176FEE195269FA6D95219A2DF738671172",
        "DepositAuth": "F64E1EABBE79D55B3BB82020516CEC2C582A98A6BFE20FBE9BB6A0D233418064",
    }

    def test_parse_rippled_amendments(cls):
        result: Any = parse_rippled_amendments("./tests/fixtures/core.h")
        cls.assertEqual(result, cls.amendment_list)
