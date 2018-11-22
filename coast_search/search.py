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

from coast_search import utils

from time import time, sleep
from datetime import date

from random_words import RandomWords
from googleapiclient.discovery import build


def replace_last(source_string, replace_what, replace_with):
    """
        DO NOT USE: This is a helper function, used by the get_random_query
        fuction.
    """
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


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
    result_list = []

    pos_topic = pos_query_segment(topic_strings)
    neg_topic = neg_query_segment(topic_strings)

    pos_reasoning = pos_query_segment(reason_indicators)
    neg_reasoning = neg_query_segment(reason_indicators)

    pos_experience = pos_query_segment(experience_indicators)
    neg_experience = neg_query_segment(experience_indicators)

    # Segment 1. !(T + E + R)
    random_query = get_random_query(topic_strings, reason_indicators, experience_indicators)

    segment_1_query = random_query + " " + neg_topic + " " + neg_reasoning + " " + neg_experience

    result_list.append({
        "segment_id": 1,
        "logic": "random + !(T+R+E)",
        "query": segment_1_query
    })

    # Segment 2. R + !(T + E)
    segment_2_query = pos_reasoning + " " + neg_topic + " " + neg_experience

    result_list.append({
        "segment_id": 2,
        "logic": "R + !(T + E)",
        "query": segment_2_query
    })

    # Segment 3. (R + E) + !T
    segment_3_query = pos_reasoning + " AND " + pos_experience + " " + neg_topic

    result_list.append({
        "segment_id": 3,
        "logic": "(R + E) + !T",
        "query": segment_3_query
    })

    # Segment 4. E + !(T + R)
    segment_4_query = pos_experience + " " + neg_topic + " " + neg_reasoning

    result_list.append({
        "segment_id": 4,
        "logic": "E + !(T + R)",
        "query": segment_4_query
    })

    # Segment 5. (T + R) + !E
    segment_5_query = pos_topic + " AND " + pos_reasoning + " " + neg_experience

    result_list.append({
        "segment_id": 5,
        "logic": "(T + R) + !E",
        "query": segment_5_query
    })

    # Segment 6. T + R + E
    segment_6_query = pos_topic + " AND " + pos_reasoning + " AND " + pos_experience

    result_list.append({
        "segment_id": 6,
        "logic": "T + R + E",
        "query": segment_6_query
    })

    # Segment 7. (T + E) + !R
    segment_7_query = pos_topic + " AND " + pos_experience + " " + neg_reasoning

    result_list.append({
        "segment_id": 7,
        "logic": "(T + E) + !R",
        "query": segment_7_query
    })

    # Semgnet 8. T + !(R + E)
    segment_8_query = pos_topic + " " + neg_reasoning + " " + neg_experience

    result_list.append({
        "segment_id": 8,
        "logic": "T + !(R + E)",
        "query": segment_8_query
    })

    # 9. Inner universe !(T + E + R) with "software engineering" as seed
    segment_9_query = '"' + seg_9_seed + '" ' + neg_topic + " " + neg_reasoning + " " + neg_experience

    result_list.append({
        "segment_id": 9,
        "logic": "seed + !(T + E + R)",
        "query": segment_9_query
    })

    return result_list





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
            sys.stdout.write(str(e))

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
    dir_path = backup_output_dir + "day_" + str(day) + "/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    timestamp = time()
    ofile = open(dir_path + str(timestamp) + ".txt", "w", encoding="utf-8")
    ofile.write(str(result))
    ofile.close()


def write_results_to_database(db, day, result):
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
    # Insert into db
    db["day_" + str(day)].insert_one(object_to_write)


def run_query(db, query_string, number_of_runs, number_of_results, api_key, search_engine_id, segment_id, day,
              backup_dir):
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
            backup_dir: A directory that can be used for storing results
                        as files.
    """
    results = []
    for i in range(0, number_of_runs):
        sys.stdout.write("Segment {0} : Running {1} out of {2} runs.\n".format(segment_id, i + 1, number_of_runs))
        results += queryAPI(query_string, number_of_results, api_key, search_engine_id, segment_id)

    # print("results:-", len(results))

    for res in results:
        write_results_to_file(day, res, backup_dir)  # as a backup incase something goes wrong
        sys.stdout.write("Segment {0} : Run {1} : Written to file.\n".format(segment_id, i + 1))

        write_results_to_database(db, day, res)
        sys.stdout.write("Segment {0} : Run {1} : Written to db.\n".format(segment_id, i + 1))


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
    db_count = db["day_" + str(day)].count()
    expected = int((number_of_results / 10) * number_of_runs * 9)

    if db_count == expected:
        sys.stdout.write("Success: expected {0} result(s), db has {1} result(s)".format(expected, db_count))
    else:
        sys.stdout.write("Failure: expected {0} result(s), db has {1} result(s)".format(expected, db_count))


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
    config = utils.get_json_from_file(config_file)

    start_date_parts = config['start_date'].split('-')
    start_date = date(int(start_date_parts[2]), int(start_date_parts[1]), int(start_date_parts[0]))

    # Get the day - starting from one
    todays_date = date.today()
    day = (todays_date - start_date).days + 1

    # Get the queries and indicators
    topic_indicators = utils.get_from_file(config['topic_file'])
    reasoning_indicators = utils.get_from_file(config['reasoning_file'])
    experience_indicators = utils.get_from_file(config['experience_file'])

    # Now generate query string for each segment
    generated_query_strings = generate_query_strings(topic_indicators, reasoning_indicators, experience_indicators)

    # Get API config and place it into list of dictionaries
    api_config = utils.get_json_from_file(config['api_details_file'])
    search_engines = api_config['search_engines']
    query_dict_list = add_api_config_to_queries(generated_query_strings, search_engines)

    db = utils.get_db(config['db_url'], config['db_client'])

    for query_object in query_dict_list:
        run_query(
            db,
            query_object['query_string'],
            config['number_of_runs'],
            config['number_of_results'],
            query_object['api_key'],
            query_object['search_engine_id'],
            query_object['segment_id'],
            day,
            config['search_backup_dir']
        )

    print("\nLaunching db check...\n")
    run_db_check(db, day, config['number_of_results'], config['number_of_runs'])
