#!/usr/bin/env python
# coding: utf-8

import json
import logging
from typing import Dict, Any, List # noqa: F401

from testing_config import BaseTestConfig
from core.rippled.utils import (
    parse_rippled_features,
)

logger = logging.getLogger('app')

class TestRippledUtils(BaseTestConfig):

    feature_list: List[str] = ['featureOwnerPaysFee', 'featureFlow', 'featureFlowCross', 'featureCryptoConditionsSuite', 'fix1513', 'featureDepositAuth', 'featureChecks', 'fix1571', 'fix1543', 'fix1623', 'featureDepositPreauth', 'fix1515', 'fix1578', 'featureMultiSignReserve', 'fixTakerDryOfferRemoval', 'fixMasterKeyAsRegularKey', 'fixCheckThreading', 'fixPayChanRecipientOwnerDir', 'featureDeletableAccounts', 'fixQualityUpperBound', 'featureRequireFullyCanonicalSig', 'fix1781', 'featureHardenedValidations', 'fixAmendmentMajorityCalc', 'featureNegativeUNL', 'featureTicketBatch', 'featureFlowSortStrands', 'fixSTAmountCanonicalize', 'fixRmSmallIncreasedQOffers', 'featureCheckCashMakesTrustLine', 'featureNonFungibleTokensV1', 'featureExpandedSignerList', 'fixNFTokenDirV1', 'fixNFTokenNegOffer', 'featureNonFungibleTokensV1_1', 'fixTrustLinesToSelf', 'fixRemoveNFTokenAutoTrustLine', 'featureImmediateOfferKilled']

    def test_parse_rippled_features(cls):
        result: Any = parse_rippled_features('./tests/fixtures/core.h')
        cls.assertEqual(result, cls.feature_list)

