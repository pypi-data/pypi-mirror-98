"""IP-API Resolver Tests."""
import json
import os
import tempfile
import unittest
import csv

from libchickadee.resolvers.iptoasn import Resolver

__author__ = 'Chapin Bryce'
__date__ = 20201003
__license__ = 'MIT Copyright 2020 Chapin Bryce'
__desc__ = '''Yet another GeoIP resolution tool.'''


class IPToASNTestCase(unittest.TestCase):
    """IPToASN Resolver Tests."""
    def setUp(self):
        """Test config"""
        self.test_data_ips = [
            '1.0.0.2', '1.0.1.0', '1.0.128.25', '1.0.140.62'
        ]
        self.expected_result = [
            {'query': '1.0.0.2', 'as': 'AS13335', 'country': 'US',
             'as_detail': 'CLOUDFLARENET - Cloudflare, Inc.'},

            {'query': '1.0.1.0', 'as': 'AS0', 'country': 'None',
             'as_detail': 'Not routed'},

            {'query': '1.0.128.25', 'as': 'AS23969', 'country': 'TH',
             'as_detail': 'TOT-NET TOT Public Company Limited'},

            {'query': '1.0.140.62', 'as': 'AS23969', 'country': 'TH',
             'as_detail': 'TOT-NET TOT Public Company Limited'}
        ]
        self.resolver = Resolver(fields=['query', 'as',
                                         'country', 'as_detail'])

    def tearDown(self):
        if os.path.exists(os.path.join(tempfile.gettempdir(), "unittest_chickadee_iptoasn_tsv_data.json")):
            os.remove(os.path.join(tempfile.gettempdir(), "unittest_chickadee_iptoasn_tsv_data.json"))

    def test_parse_iptoasn_tsv(self):
        expected = [
            {"range_start": "1.0.0.0", "range_end": "1.0.0.255", "as": "13335", "country": "US",
             "as_detail": "CLOUDFLARENET - Cloudflare, Inc.", "range_start_int": 16777216, "range_end_int": 16777471},
            {"range_start": "1.0.1.0", "range_end": "1.0.3.255", "as": "0", "country": "None",
             "as_detail": "Not routed", "range_start_int": 16777472, "range_end_int": 16778239}
        ]
        actual = self.resolver.parse_tsv('test_data/ip2asn-combined.sample.tsv')
        self.assertEqual(10, len(actual))
        self.assertDictEqual(expected[0], actual[0])
        self.assertDictEqual(expected[1], actual[1])

    def test_cache_parsed_data(self):
        expected = [
            {"range_start": "1.0.0.0", "range_end": "1.0.0.255", "as": "13335", "country": "US",
             "as_detail": "CLOUDFLARENET - Cloudflare, Inc.", "range_start_int": 16777216, "range_end_int": 16777471},
            {"range_start": "1.0.1.0", "range_end": "1.0.3.255", "as": "0", "country": "None",
             "as_detail": "Not routed", "range_start_int": 16777472, "range_end_int": 16778239}
        ]
        if self.resolver.cache_file_exists("unittest_chickadee_iptoasn_tsv_data.json"):
            os.remove(os.path.join(tempfile.gettempdir(), "unittest_chickadee_iptoasn_tsv_data.json"))
        actual = self.resolver.build_cache(expected, cache_name="unittest_chickadee_iptoasn_tsv_data.json")

        self.assertTrue(actual)

        with open(os.path.join(tempfile.gettempdir(), "unittest_chickadee_iptoasn_tsv_data.json")) as actual_file:
            actual_data = json.load(actual_file)
        self.assertDictEqual(actual_data[0], expected[0])
        self.assertDictEqual(actual_data[1], expected[1])
