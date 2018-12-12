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


    def test_write_to_file_json(self):

        test_dict = {1: 'a', 2: 'b', 'c': 3}
        search.write_to_file("test_file", test_dict, "/Users/liz/Local/coast_search/tests/test_output/", ".json")


    def test_write_to_file_txt(self):
        test_string = "test string wow"
        search.write_to_file("test_file", test_string, "/Users/liz/Local Documents/Work/coast_search/tests/test_output", ".txt")

    def test_extract_search_results_from_JSON(self):
        filename = "/Users/liz/Local Documents/Work/coast_search/tests/test_data/results_for_testing_extraction.json"
        json_data = utils.get_json_from_file(filename)

        result = search.extract_search_results_from_JSON(json_data)
        expected = utils.get_json_from_file('/Users/liz/Local Documents/Work/coast_search/tests/test_data/expected_results.json')

        self.assertEqual(expected, result)

    def test_deduplicate_urls_no_repetiton_between_segments(self):
        filename = "/Users/liz/Local/coast_search/tests/test_data/results_for_testing_dedup.json"
        json_data = utils.get_json_from_file(filename)
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
        filename = "/Users/liz/Local/coast_search/tests/test_data/results_for_testing_dedup_between_seg.json"
        json_data = utils.get_json_from_file(filename)
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


