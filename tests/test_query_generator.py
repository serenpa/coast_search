#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_citations
----------------------------------
Tests for `citations` module.
"""
import os
import unittest

from coast_search import query_generator


class TestQueryGenerator(unittest.TestCase):

    def setUp(self):
        self.dimensions_dict = {
            "reasoning": ['because', 'however', 'conclude', 'but', 'for example'],
            "experience": ['i', 'me', 'our', 'we', 'in my experience'],
            "topic": ['trustworthy', 'software']
        }

        self.one_dimension_queries = [
            {'segment_id': 2, 'logic': 'topic', 'query': '("credibility" OR "assessment")'},
            {'segment_id': 0, 'logic': 'random + !(topic)', 'query': '"annexs mug regions" -"credibility" -"assessment" '},
            {'segment_id': 1, 'logic': 'seed + !(topic)', 'query': '"software" -"credibility" -"assessment" '}
        ]

        self.three_search_engines = [
            {
                "name": "cse-1",
                "api_key": "aaa2fcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:aaa"
            },
            {
                "name": "cse-2",
                "api_key": "bbb2fcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:bbb"
            },
            {
                "name": "cse-3",
                "api_key": "cccfcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:ccc"
            }]

    def test_generate_result_list_one_dimension(self):
        one_dimension_data = {
            'topic': {
            'wordsList': ['credibility', 'assessment'],
            'pos': '("credibility" OR "assessment")',
            'neg': '-"credibility" -"assessment" '
            }
        }

        actual_1_dimension = query_generator.generate_result_list(one_dimension_data,
                                                                  ["topic"],
                                                                  "software",
                                                                  "annexs mug regions")

        self.assertEqual(self.one_dimension_queries, actual_1_dimension)

    def test_add_api_config_1D_unique_keys(self):

        search_engines = self.three_search_engines

        expected = [
            {
                'segment_id': 2,
                 'logic': 'topic',
                 'query': '("credibility" OR "assessment")',
                 "se_name": "cse-1",
                 "api_key": "aaa2fcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                 "search_engine_id": "82260244545522837893:aaa"
             },
            {
                'segment_id': 0,
                'logic': 'random + !(topic)',
                'query': '"annexs mug regions" -"credibility" -"assessment" ',
                "se_name": "cse-2",
                "api_key": "bbb2fcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:bbb"
            },
            {
                'segment_id': 1,
                'logic': 'seed + !(topic)',
                'query': '"software" -"credibility" -"assessment" ',
                "se_name": "cse-3",
                "api_key": "cccfcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:ccc"
            }
        ]

        actual = query_generator.add_api_config_to_queries(self.one_dimension_queries, search_engines)

        self.assertEqual(expected, actual)

    def test_add_api_config_1D_one_key(self):

        search_engines = self.three_search_engines[0:1]

        expected = [
            {
                'segment_id': 2,
                'logic': 'topic',
                'query': '("credibility" OR "assessment")',
                "se_name": "cse-1",
                "api_key": "aaa2fcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:aaa"
            },
            {
                'segment_id': 0,
                'logic': 'random + !(topic)',
                'query': '"annexs mug regions" -"credibility" -"assessment" ',
                "se_name": "cse-1",
                "api_key": "aaa2fcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:aaa"
            },
            {
                'segment_id': 1,
                'logic': 'seed + !(topic)',
                'query': '"software" -"credibility" -"assessment" ',
                "se_name": "cse-1",
                "api_key": "aaa2fcb8f-9c52-44b9-8a71-6d7dcdbfdbd8",
                "search_engine_id": "82260244545522837893:aaa"
            }
        ]

        actual = query_generator.add_api_config_to_queries(self.one_dimension_queries, search_engines)

        self.assertEqual(expected, actual)

    def test_add_api_config_1D_incorrect_keys(self):
        search_engines = self.three_search_engines[0:2]

        self.assertRaises(Exception, query_generator.add_api_config_to_queries, self.one_dimension_queries, search_engines)

    def test_check_length(self):

        self.assertRaises(Exception, query_generator.check_length,"seed", "random", self.dimensions_dict, 5)

        self.assertRaises(Exception, query_generator.check_length, "seed", "random", self.dimensions_dict, 25)

        expect_pass = query_generator.check_length("seed", "random", self.dimensions_dict, 50)
        self.assertTrue(expect_pass)

        expect_pass_border = query_generator.check_length("seed", "random", self.dimensions_dict, 26)
        self.assertTrue(expect_pass_border)
