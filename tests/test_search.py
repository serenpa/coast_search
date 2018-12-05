#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_search
----------------------------------
Tests for `search` module.
"""

import unittest

from coast_search import search
from coast_search import utils


class TestSearch(unittest.TestCase):

    # def setUp(self):
        # self.dimensions_dict = {
        #     "reasoning": ['because', 'however', 'conclude', 'but', 'for example'],
        #     "experience": ['i', 'me', 'our', 'we', 'in my experience'],
        #     "topic": ['trustworthy', 'software']
        # }

    def test_write_to_json(self):

        test_dict = {1: 'a', 2: 'b', 'c': 3}

        search.write_to_json("test_file", test_dict, "/Users/liz/Local Documents/Work/coast_search/tests/test_output", ".json")

    def test_extract_search_results_from_JSON(self):
        filename = "/Users/liz/Local Documents/Work/coast_search/tests/test_data/results_for_testing_extraction.json"

        result = search.extract_search_results_from_JSON(filename)
        expected = utils.get_json_from_file('/Users/liz/Local Documents/Work/coast_search/tests/test_data/expected_results.json')

        self.assertEqual(expected, result)

    def test_deduplicate_urls(self):
        filename = ""


