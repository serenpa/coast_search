#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------
Tests for `utils` module.
"""
import os
import unittest

from coast_search import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.file_path_prefix = os.path.dirname(__file__) + "/test_data/search_dimensions/"

    def test_get_from_file_list(self):
        file_list = [self.file_path_prefix + "reasoning.txt",
                     self.file_path_prefix + "experience.txt",
                     self.file_path_prefix + "topic.txt"]

        expected_dict = {
            "reasoning": ['because', 'however', 'conclude', 'but', 'for example'],
            "experience": ['i', 'me', 'our', 'we', 'in my experience'],
            "topic": ['trustworthy', 'software']
        }

        actual_dict = utils.get_from_file_list(file_list)
        self.assertEqual(actual_dict, expected_dict)


