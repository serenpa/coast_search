"""
    Title: search_command.py
    Author: Ashley Williams
    Description: A collection of functions that can be used for running
    searches. This module calls is called by init, so there is no need to
    import this module specifically.
    Refer to the documentation for details of how to use this module
    (http://coast_search.readthedocs.io/).
"""
import sys
import os
import logging

from coast_search import utils
from coast_search import query_generator

from time import time, sleep
from datetime import date

from googleapiclient.discovery import build





def queryAPI(query, number_of_results, api_key, search_engine_id, segment_id):
    """
        Query the API, return the results as a list of JSON objects.
        Refer to the documentation for usage guidelines and descriptions of
        what each parameter means (http://coast_search.readthedocs.io/).
        Args:
            query: The query string to run.
            number_of_results: The number of results you wish to be returned.
                               Note, the free version of the Custom Search API
                               is limited to 100 searches per day. Each search
                               returns 10 results.
            api_key: The api key of the search engine, provided by Google.
            search_engine_id: The id of the Custom Search Engine provided by
                              Google.
            segment_id: The segment which the results belong to.
        Returns:
            results_list: The results from Google as a list of JSON objects
        Err:
            In the event of an error, the error is printed to the stdout.
    """
    service = build("customsearch", "v1", developerKey=api_key)

    result_list = []

    # make multiple api calls in multiples of 10 to get number of results
    for i in range(0, number_of_results, 10):
        i += 1
        # print("i: " + str(i))

        try:
            api_call = service.cse().list(
                q=query,
                cx=search_engine_id,
                start=i
            )

            #TODO: make the sleep time configurable (we wait between queries so that google dont think we're a robot)
            sleep(1)
            result = api_call.execute()

            result_list.append({
                "query": query,
                "number_of_results": number_of_results,
                "api_key": api_key,
                "search_engine_id": search_engine_id,
                "segment_id": segment_id,
                "response": result
            })
        except Exception as e:
            raise Exception(str(e))

    return result_list


def write_results_to_file(day, result, backup_output_dir):
    """
        Writes the results to a txt file, just incase something goes wrong with
        writing to the database.
        Args:
            day: The day of the search period that the result has originated
                 from.
            result: The output from running the query.
            backup_output_dir: A directory that can be used for storing results
                               as files.
    """
    #todo get rid of this
    dir_path = backup_output_dir + "day_" + str(day) + "/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    timestamp = time()
    ofile = open(dir_path + str(timestamp) + ".txt", "w", encoding="utf-8")
    ofile.write(str(result))
    ofile.close()


def write_to_file(name, result, dir, extension):
        """
            Writes to results to a file
            Args:
                day: The day of the search period that the result has originated
                     from.
                result: The output from running the query.
                backup_output_dir: A directory that can be used for storing results
                                   as files.
        """
        dir_path = dir + name + "/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        timestamp = time()
        ofile = open(dir_path + str(timestamp) + extension, "w", encoding="utf-8")
        ofile.write(str(result))
        ofile.close()


def get_object_to_write(result):
    """
        Writes the results to the db, for later analysis.
        Args:
            db: The pymongo db object.
            day: The day of the search period that the result has originated
                 from.
            result: The output from running the query.
    """
    result_items = []
    urls = []

    if "items" in result["response"].keys():
        se_items = result["response"]["items"]

        for item in se_items:
            title = item["title"]
            link = item["link"]

            result_items.append({
                "title": title,
                "link": link
            })

            urls.append(link)

    request_data = []

    requests = result["response"]["queries"]["request"]

    for req in requests:
        request_data.append({
            "request_cx": req["cx"],
            "request_count": req["count"],
            "total_results": req["totalResults"],
            "start_index": req["startIndex"],
            "search_terms": req["searchTerms"]
        })

    object_to_write = {
        "segment_id": result["segment_id"],
        "query_string": result["query"],
        "api_info": {
            "api_key": result["api_key"],
            "search_engine_id": result["search_engine_id"]
        },
        "number_of_results_specified": result["number_of_results"],
        "response_info": {
            "search_info_total_results": result["response"]["searchInformation"]["totalResults"],
            "search_time": result["response"]["searchInformation"]["searchTime"],
            "url_template": result["response"]["url"]["template"],
            "requests": request_data
        },
        "results": result_items,
        "links": urls
    }

    return object_to_write


def run_query(query_string, number_of_runs, number_of_results, api_key, search_engine_id, segment_id, day,
              backup_dir):
    """
        Runs the query against the Google Custom Search API.
        Refer to the documentation for usage guidelines and descriptions of
        what each parameter means (http://coast_search.readthedocs.io/).
        Args:
            db: The pymongo db object.
            query_string: The query string to run.
            number_of_runs: The number of runs you wish to be repeat for each
                            day. Notfig = utils.get_json_from_file(config['api_details_file']e, the free version of the Custom Search API
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
            backup_dir: A directory that can be used for storing results
                        as files.
    """
    results = []
    for i in range(0, number_of_runs):
        #todo change to logger
        print(query_string)
        sys.stdout.write("Segment {0} : Running {1} out of {2} runs.\n".format(segment_id, i + 1, number_of_runs))
        results += queryAPI(query_string, number_of_results, api_key, search_engine_id, segment_id)

    # print("results:-", len(results))

    extracted_results = []

    for res in results:
        #todo update to use new write to file method
        write_results_to_file(day, res, backup_dir)  # as a backup incase something goes wrong
        logging.info("Segment {0} : Run {1} : Written to file.\n".format(segment_id, i + 1))

        extracted_results.append(get_object_to_write(res))
        logging.info("Segment {0} : Run {1} : Written to db.\n".format(segment_id, i + 1))

    return extracted_results


def run_daily_search(config_file, write_to_file_flag):
    """
        Run a full daily search. This function can be set up as a cronjob
        (or scheduled task on Windows) to search over consecutive days.
        Refer to the documentation for usage guidelines and descriptions of
        how the config file should be structured (http://coast_search.readthedocs.io/).
        Args:
            config_file: Path to a JSON file containing all relevant information for
                         conducting the searches.
            write_to_file_flag: boolean flag for writing to file
    """
    config = utils.get_json_from_file(config_file)

    logging.basicConfig(filename=config["logging_dir"])

    day = utils.number_of_days_past_start_date(config)

    # Get the queries and indicators
    dimensions_dict = utils.get_from_file_list(config['dimensions'])

    # Now generate query string for each segment
    generated_query_strings = query_generator.generate_query_strings_n_dimensions(dimensions_dict, "software", 32)

    # Get API config and place it into list of dictionaries
    api_config = utils.get_json_from_file(config['api_details_file'])
    search_engines = api_config['search_engines']
    # yikes_generated_from_old = [{'segment_id': 1, 'logic': 'random + !(T+R+E)', 'query': '"coughs abrasive abettor" -"credibility" -"assessment"  -"because" -"however" -"conclude" -"but"  -"i" -"our" -"experience" -"my" '},
    #                             {'segment_id': 2, 'logic': 'R + !(T + E)', 'query': '("because" OR "however" OR "conclude" OR "but") -"credibility" -"assessment"  -"i" -"our" -"experience" -"my" '},
    #                             {'segment_id': 3, 'logic': '(R + E) + !T', 'query': '("because" OR "however" OR "conclude" OR "but") AND ("i" OR "our" OR "experience" OR "my") -"credibility" -"assessment" '},
    #                             {'segment_id': 4, 'logic': 'E + !(T + R)', 'query': '("i" OR "our" OR "experience" OR "my") -"credibility" -"assessment"  -"because" -"however" -"conclude" -"but" '},
    #                             {'segment_id': 5, 'logic': '(T + R) + !E', 'query': '("credibility" OR "assessment") AND ("because" OR "however" OR "conclude" OR "but") -"i" -"our" -"experience" -"my" '},
    #                             {'segment_id': 7, 'logic': '(T + E) + !R', 'query': '("credibility" OR "assessment") AND ("i" OR "our" OR "experience" OR "my") -"because" -"however" -"conclude" -"but" '},
    #                             {'segment_id': 8, 'logic': 'T + !(R + E)', 'query': '("credibility" OR "assessment") -"because" -"however" -"conclude" -"but"  -"i" -"our" -"experience" -"my" '},
    #                             {'segment_id': 9, 'logic': 'seed + !(T + E + R)', 'query': '"software" -"credibility" -"assessment"  -"because" -"however" -"conclude" -"but"  -"i" -"our" -"experience" -"my" '}]
    query_dict_list = query_generator.add_api_config_to_queries(generated_query_strings, search_engines)
    #query_dict_list = query_generator.add_api_config_to_queries(yikes_generated_from_old, search_engines)
    results = append_daily_search_results(
        query_dict_list,
        config['number_of_runs'],
        config['number_of_results'],
        day,
        config['search_backup_dir'],
    )

    if write_to_file_flag:
        name = "_results_day_" + str(day)
        write_to_file(name, results, config['results_output_dir'], ".json")

    return results


### TODO: update documentation
def append_daily_search_results(query_dict_list, number_of_runs, number_of_results, day, search_backup_dir): #flag goes here):
    """
        Run a full daily search. This function can be set up as a cronjob
        (or scheduled task on Windows) to search over consecutive days.
        Refer to the documentation for usage guidelines and descriptions of
        how the config file should be structured (http://coast_search.readthedocs.io/).
        Args:
            config_file: Path to a JSON file containing all relevant information for
                         conducting the searches.
    """

    results = []

    for query_object in query_dict_list:
        results.append(run_query(
            query_object['query'],
            number_of_runs,
            number_of_results,
            query_object['api_key'],
            query_object['search_engine_id'],
            query_object['segment_id'],
            day,
            search_backup_dir
        ))

    return {
        "results": results
    }
