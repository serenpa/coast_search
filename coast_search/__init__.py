"""
    Title: search __init__
    Author: Ashley Williams
    Description: A collection of functions that can be used for running
    searches. Refer to the documentation for details of how to use this module
    (http://coast_search.readthedocs.io/).
"""
from coast_search.search import search
# -*- coding: utf-8 -*-
from __future__ import print_function
from ._version import get_versions

__author__ = 'Ashley Williams'
__email__ = 'ashley.williams@pg.canterbury.ac.nz'
__version__ = get_versions()['version']
del get_versions

def generate_query_strings(topic_strings, reason_indicators, experience_indicators, seg_9_seed="software engineering"):
    """
        Generates the query string for each segment and returns as a list of
        dict objects in the following format:
        [{
            segment_id: 6,
            logic: "T+R+E",
            query: query string here
        }]
        Notes:
            1. Topic phrases stay as phrases, multple topic words are AND'd
               together.
            2. The seg_9_seed parameter is optional, the default will be
               "software engineering"
        Segments:
            1. !(T + E + R)
            2. R + !(T + E)
            3. (R + E) + !T
            4. E + !(T + R)
            5. (T + R) + !E
            6. T + R + E
            7. (T + E) + !R
            8. T + !(R + E)
            9. Inner universe !(T + E + R) with "software engineering" as seed
        Args:
            topic_strings: The topic strings being used for the search.
            reasoning_indicators: The reasoning indicators being used for the
                                  search.
            experience_indicators: The experience indicators being used for the
                                   search.
            seg_9_seed: The seed word for segment 9 queries. The default is
                        "software engineering"
        Returns:
            result_list: a list of objects, each stating the segment_id, search
                         logic, and query string.
    """
    return search.generate_query_strings(topic_strings, reason_indicators, experience_indicators, seg_9_seed)


def add_api_config_to_queries(generated_query_strings, search_engines):
    """
        Merges the two parameters and returns a list of dicts that include the
        api config.
        Args:
            generated_query_strings: The output from the generate_query_strings
                                     function.
            search_engines: The search engines list that is found in the
                            api_config file. See the documentation for usage
                            guidelines (http://coast_search.readthedocs.io/).
        Returns:
            result_list: A modified version of the output from the
                         generate_query_strings function. The list will now
                         also contain the required api config.
    """
    return search.add_api_config_to_queries(generated_query_strings, search_engines)


def run_query(db, query_string, number_of_runs, number_of_results, api_key, search_engine_id, segment_id, day):
    """
        Runs the query against the Google Custom Search API.
        Refer to the documentation for usage guidelines and descriptions of
        what each parameter means (http://coast_search.readthedocs.io/).
        Args:
            db: The pymongo db object.
            query_string: The query string to run.
            number_of_runs: The number of runs you wish to be repeat for each
                            day. Note, the free version of the Custom Search API
                            is limited to 100 searches per day. Each search
                            returns 10 results.
            number_of_results: The number of results you wish to be returned.
                               Note, the free version of the Custom Search API
                               is limited to 100 searches per day. Each search
                               returns 10 results.
            api_key: The api key of the search engine, provided by Google.
            search_engine_id: The id of the Custom Search Engine provided by
                              Google.
            segment_id: The segment which the results belong to.
            day: The day of the search period that the result has originated
                 from.
    """
    search.run_query(db, query_string, number_of_runs, number_of_results, api_key, search_engine_id, segment_id, day)


def run_db_check(db, day, number_of_results, number_of_runs):
    """
        Logs whether the number of expected results matches the actual results.
        Refer to the documentation for usage guidelines and descriptions of
        what each parameter means (http://coast_search.readthedocs.io/).
        Args:
            db: The pymongo db object.
            day: The day of the search period that the result has originated
                 from.
    """
    search.run_db_check(db, day, number_of_results, number_of_runs)



def run_daily_search(config_file):
    """
        Run a full daily search. This function can be set up as a cronjob
        (or scheduled task on Windows) to search over consecutive days.
        Refer to the documentation for usage guidelines and descriptions of
        how the config file should be structured (http://coast_search.readthedocs.io/).
        Args:
            config_file: A JSON file containing all relevant information for
                         conducting the searches.
    """
    search.run_daily_search(config_file)
