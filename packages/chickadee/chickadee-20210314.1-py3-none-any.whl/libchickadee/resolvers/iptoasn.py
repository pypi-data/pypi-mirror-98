import json
import logging
import csv
import os
import tempfile
from tempfile import NamedTemporaryFile

import netaddr

from . import ResolverBase

logger = logging.getLogger(__name__)

__author__ = 'Chapin Bryce'
__date__ = 20201003
__license__ = 'MIT Copyright 2020 Chapin Bryce'
__desc__ = '''Yet another GeoIP resolution tool.'''

FIELDS = [
    'query', 'count', 'as', 'country', 'as_detail'
]


class Resolver(ResolverBase):
    """Class to handle resolutions of IP addressed against TSV files from iptoasn.com.

    Specifically parses data from the combined IPv4 and IPv6 TSV file.

    Args:
        fields (list): Collection of fields to request in resolution.
        lang (str): Language for returned results.
    """
    def __init__(self, fields=None, lang='en'):
        """Initialize class object and configure default values."""
        self.supported_langs = ['en']
        super().__init__()

    @classmethod
    def parse_tsv(cls, tsv_path):
        """Convert TSV data in to a format we can query

        This file should originate from https://iptoasn.com/ and contain the fields
            range_start, range_end, AS_number, country_code, and AS_description

        Args:
            tsv_path (str): Path to TSV file to read

        Returns:
            (dict): Dictionary of loaded TSV data
        """

        dataset = []
        with open(tsv_path, 'r') as open_file:
            csv_file = csv.reader(open_file, delimiter='\t')
            for raw_line in csv_file:
                dataset.append({
                    "range_start": raw_line[0],
                    "range_start_int": cls.get_ip_int(raw_line[0]),
                    "range_end": raw_line[1],
                    "range_end_int": cls.get_ip_int(raw_line[1]),
                    "as": raw_line[2],
                    "country": raw_line[3],
                    "as_detail": raw_line[4],
                })
        return dataset

    @staticmethod
    def get_ip_int(ip_addr):
        return int(netaddr.IPAddress(ip_addr))

    @staticmethod
    def cache_file_exists(cache_file_name):
        return os.path.exists(cache_file_name)

    def build_cache(self, tsv_data, cache_name="chickadee_iptoasn_tsv_data.json"):
        cache_file_path = os.path.join(tempfile.gettempdir(), cache_name)
        if self.cache_file_exists(cache_file_path):
            # The cache file exists
            # TODO confirm whether or not the cache is expired
            return True
        try:
            with open(cache_file_path, 'w') as open_cache_file:
                json.dump(tsv_data, open_cache_file)
            return True
        except Exception as e:
            logger.exception("An exception was encountered when building the cache.", exc_info=e)
            logger.warning("Please report the above exception this log file to https://github.com/chapinb/chickadee")
        return False
