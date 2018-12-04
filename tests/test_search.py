#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_search
----------------------------------
Tests for `search` module.
"""
import os
import unittest
import json
import ast

from coast_search import search
from coast_search import utils


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.dimensions_dict = {
            "reasoning": ['because', 'however', 'conclude', 'but', 'for example'],
            "experience": ['i', 'me', 'our', 'we', 'in my experience'],
            "topic": ['trustworthy', 'software']
        }

    def test_write_to_json(self):

        test_dict = {1: 'wow', 2: 'yikes', 'yeet': 3}

        search.write_to_json("test_file", test_dict, "/Users/liz/Local Documents/Work/coast_search/tests/test_output", ".json")

    def test_extract_search_results_from_JSON(self):
        filename = "/Users/liz/Local Documents/Work/coast_search/tests/test_data/results_for_testing_extraction.json"

        result = search.extract_search_results_from_JSON(filename)
        print("\n ACTUAL")
        print(result)

        expected = utils.get_json_from_file('/Users/liz/Local Documents/Work/coast_search/tests/test_data/expected_results.json')
        print("\n EXPECTED")
        print(expected)
        self.assertEqual(expected, result)

        # expected = {"search_results": [{
        #   "url": url,
        #   "title": title,
        #   "segment_id": segment_id,
        #   "query": query,
        #   "total_results": total_results,
        #   "source_collection": coll, # maybe not needed
        #   "item": item,
        #   "response": r
        # }, {}, {}]
        # }




        # res = res.replace("\'", "\"")
        # print(res)
        # res = 'r"""' + res
        # print(res)
        # y = json.loads(res)
        # print(y)

        # print("\n\n********\n\n")
        # print(data[0])
        # print("\n\n********\n\n")
        # pprint.pprint(data[0])



    # def test_generate_result_list_one_dimension(self):
    #     one_dimension_data = {
    #         'topic': {
    #         'wordsList': ['credibility', 'assessment'],
    #         'pos': '("credibility" OR "assessment")',
    #         'neg': '-"credibility" -"assessment" '
    #         }
    #     }
    #
    #     actual_1_dimension = query_generator.generate_result_list(one_dimension_data,
    #                                                               ["topic"],
    #                                                               "software",
    #                                                               "annexs mug regions")
    #
    #     self.assertEqual(self.one_dimension_queries, actual_1_dimension)


