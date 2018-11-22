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
from coast_search import utils


class TestQueryGenerator(unittest.TestCase):

    def setUp(self):
        self.dimensions_dict = {
            "reasoning": ['because', 'however', 'conclude', 'but', 'for example'],
            "experience": ['i', 'me', 'our', 'we', 'in my experience'],
            "topic": ['trustworthy', 'software']
        }


    def test_generate_result_list(self):
        # todo
        print("") #api_details_file
        # generate_result_list(dimensions_data, dimensions, seed, random)



    def test_generate_query_strings_n_dimensions(self):
        # todo
        print("")
        # generate_query_strings_n_dimensions

    def test_check_length(self):

        expect_fail = query_generator.check_length("seed", "random", self.dimensions_dict, 5)
        self.assertFalse(expect_fail)

        expect_fail_border = query_generator.check_length("seed", "random", self.dimensions_dict, 25)
        self.assertFalse(expect_fail_border)

        expect_pass = query_generator.check_length("seed", "random", self.dimensions_dict, 50)
        self.assertTrue(expect_pass)

        expect_pass_border = query_generator.check_length("seed", "random", self.dimensions_dict, 26)
        self.assertTrue(expect_pass_border)
