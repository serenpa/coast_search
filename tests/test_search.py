#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_search
----------------------------------
Tests for `search` module.
"""

import unittest
import os

from coast_search import search
from coast_search import utils


class TestSearch(unittest.TestCase):

    def setUp(self):
        # using abspath means there is consistency between running running ```python setup.py test``` and tests
        # through ide
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.test_data_folder_location = os.path.join(cwd, "test_data/")

    def test_write_to_file_json(self):
        # I wrote these to produce a file that I then manually checked.
        test_dict = {1: 'a', 2: 'b', 'c': 3}
        search.write_to_file("test_file", test_dict, "../tests/test_output/", ".json")

    def test_write_to_file_txt(self):
        test_string = "test string wow"
        search.write_to_file("test_file", test_string, "../tests/test_output", ".txt")

    def test_extract_search_results_from_JSON(self):
        filename = "results_for_testing_extraction.json"
        filepath = os.path.join(self.test_data_folder_location, filename)
        json_data = utils.get_json_from_file(filepath)

        result = search.extract_search_results_from_JSON(json_data)
        expected_results_filename = "expected_results.json"
        expected_results_filpath = os.path.join(self.test_data_folder_location, expected_results_filename)
        expected = utils.get_json_from_file(expected_results_filpath)

        self.assertEqual(expected, result)

    def test_deduplicate_urls_no_repetiton_between_segments(self):
        filename = "results_for_testing_dedup.json"
        filepath = os.path.join(self.test_data_folder_location, filename)

        json_data = utils.get_json_from_file(filepath)
        deduplicated_urls_object = search.deduplicate_urls(json_data)
        deduplicated_urls_list = deduplicated_urls_object["deduplicated_urls"]

        expected = [
            "https://medium.com/s/story/whats-wrong-with-software-development-language-cart-before-the-engineering-horse-c477df24e94d",
            "https://www.msnbc.com/msnbc/watch/apple-ceo-tim-cook-learning-to-code-is-important-because-software-touches-everything-we-do-1204860483791",
            "https://writingcooperative.com/im-a-software-engineer-not-a-writer-but-i-want-to-write-6fa9af8290b6",
            "https://www.eetimes.com/author.asp?section_id=36&doc_id=1329106",
            "https://www.because-software.com/",
            "https://en.wikipedia.org/wiki/Therac-25",
            "https://kb.iu.edu/d/afdk",
            "https://en.wikipedia.org/wiki/Freeware"
        ]
        expected.sort()
        deduplicated_urls_list.sort()

        self.assertEqual(expected, deduplicated_urls_list)
        self.assertRaises(KeyError, lambda: deduplicated_urls_object["warning"])

    def test_deduplicate_urls_repetiton_between_segments(self):
        filename = "results_for_testing_dedup_between_seg.json"
        filepath = os.path.join(self.test_data_folder_location, filename)

        json_data = utils.get_json_from_file(filepath)
        deduplicated_urls_object = search.deduplicate_urls(json_data)
        deduplicated_urls_list = deduplicated_urls_object["deduplicated_urls"]

        expected = [
            "https://medium.com/s/story/whats-wrong-with-software-development-language-cart-before-the-engineering-horse-c477df24e94d",
            "https://www.msnbc.com/msnbc/watch/apple-ceo-tim-cook-learning-to-code-is-important-because-software-touches-everything-we-do-1204860483791",
            "https://writingcooperative.com/im-a-software-engineer-not-a-writer-but-i-want-to-write-6fa9af8290b6",
            "https://www.eetimes.com/author.asp?section_id=36&doc_id=1329106",
            "https://www.because-software.com/",
            "https://en.wikipedia.org/wiki/Therac-25",
            "https://kb.iu.edu/d/afdk",
            "https://kb.iu.edu/d/afdk",
            "https://en.wikipedia.org/wiki/Freeware"
        ]
        expected.sort()
        deduplicated_urls_list.sort()

        self.assertEqual(expected, deduplicated_urls_list)
        self.assertEqual("same url found across more than 1 segment", deduplicated_urls_object["warning"]["message"])
        self.assertEqual(["https://kb.iu.edu/d/afdk"], deduplicated_urls_object["warning"]["urls"])
        self.assertEqual([2, 3], deduplicated_urls_object["warning"]["segments"])
