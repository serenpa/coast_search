"""
    Title: coast_search

    Author: Ashley Williams

    Description: COAST_SEARCH allows you to generate and run queries against the Google Custom Search API.
"""
from __future__ import print_function
from ._version import get_versions

from coast_search import query_generator
from coast_search import search
from coast_search import utils

__author__ = 'Ashley Williams'
__email__ = 'ashley.williams@pg.canterbury.ac.nz'
__version__ = get_versions()['version']
del get_versions
