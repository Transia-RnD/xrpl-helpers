#!/usr/bin/env python
# coding: utf-8

# import json
import logging
from typing import Dict, Any  # noqa: F401

from testing_config import BaseTestConfig
from xrpl_helpers.common.utils import (
    read_file,
    read_json,
    write_json,
    read_yaml
)

logger = logging.getLogger('app')


class TestCommonUtils(BaseTestConfig):

    def test_read_file(cls):
        result: Dict[str,  Any] = read_file('./tests/fixtures/core.h')
        cls.assertIsNotNone(result)

    def test_read_json(cls):
        result: Dict[str,  Any] = read_json('./tests/fixtures/core.json')
        cls.assertIn("test", result)
        cls.assertEqual(result["test"], "success")

    def test_write_json(cls):
        json_data = { 'test': 'success' }
        result: bool = write_json(json_data, './tests/fixtures/core.json')
        cls.assertTrue(result)

    def test_read_yaml(cls):
        json_data = { 'test': 'success' }
        result: str = read_yaml('./tests/fixtures/core.yml')
        cls.assertIn("apiVersion", result)
        cls.assertIn("kind", result)
        cls.assertIn("metadata", result)
        cls.assertEqual(result["apiVersion"], "networking.gke.io/v1")
