"""
    Contains the functions required for generating the multiple queries
    from the config, given n number of dimensions and any constraints
"""

from random_words import RandomWords
import json
import itertools
import functools


def get_random_query(words_to_exclude):
    """
    Segment 1 uses a random seed query. This function creates that seed
    query using the random_words library and returns it.
    Notes:
        1. The random query returned wont contain any word that exists in
        any topic string or indicator list.
        2. The random query string will always be three words long.
    Args:
        words_to_exclude: the list of words from each of the dimensions to use as stoplist
    Returns:
        qs: The generated random query.
    """

    stop_list = words_to_exclude

    rw = RandomWords()

    flag = False

    while (flag == False):
        words = rw.random_words(count=3)

        flag2 = True
        for word in words:
            if word in stop_list:
                flag2 = False

        if flag2 == True:
            flag = True

        # print(words)

    qs = '"'
    for word in words:
        qs += word + ' '

    # Replace final space with quote
    qs = qs[:-1]
    qs += '"'

    return qs


def pos_query_segment(phrase_list):
    """
        Given a list of phrases, returns a string of all the phrases AND'd
        together.
        e.g. ("but" AND "because" AND "however")
        Args:
            phrase_list: a list of phrases (e.g. reasoning/experience
                         indicators)
        Returns:
            result_string: a string of all phrases AND'd together ready for a
                           search engine.
    """
    result_string = "("

    for phrase in phrase_list:
        result_string += '"' + phrase + '" OR '

    # Now remove the last AND
    result_string = result_string[:-4]
    result_string += ")"

    return result_string


def neg_query_segment(phrase_list):
    """
        Given a list of phrases, returns a string of all the phrases negated.
        e.g. -"but" -"because" -"however"
        Args:
            phrase_list: a list of phrases (e.g. reasoning/experience
                         indicators)
        Returns:
            result_string: a string of all phrases AND'd together ready for a
                           search engine.
    """
    result_string = ""

    for phrase in phrase_list:
        result_string += '-"' + phrase + '" '

    return result_string


def generate_result_list(dimensions_data, dimensions, seed, random):
    """
    Given the dimensions information, dynamically generates logic & query for each segment.

    Note: segment 0 will always contain the random query, and segment 1 will always contain the seed.

    Args:
        dimensions_data: a list of phrases (e.g. reasoning/experience
                     indicators)
    Returns:
        result_string: a string of all phrases AND'd together ready for a
                       search engine.
    """
    combinations = functools.reduce(lambda x, y: list(itertools.combinations(dimensions, y)) + x,
                                    range(len(dimensions) + 1), [])
    result_list = []
    segment_count = 2  # starts at 2, as we always want 0 and 1 to be specific

    for tup in combinations:
        diff = list(set(dimensions).difference(set(tup)))
        positives = [dimensions_data[x]["pos"] for x in tup]
        negatives = [dimensions_data[x]["neg"] for x in diff]

        if diff:
            if tup:
                query_string = " AND ".join(positives) + " " + "".join(negatives)
                logic_string = " + ".join(tup) + " + " + "!(" + " + ".join(diff) + ")"

                result_list.append({
                    "segment_id": segment_count,
                    "logic": logic_string,
                    "query": query_string
                })
                segment_count += 1
            else:
                result_list.append({
                    "segment_id": 0,
                    "logic": "random + !(" + " + ".join(diff) + ")",
                    "query": '"' + random + '"' + "".join(negatives)
                })

                result_list.append({
                    "segment_id": 1,
                    "logic": "seed + !(" + " + ".join(diff) + ")",
                    "query": '"' + seed + '" ' + "".join(negatives)
                })
        else:
            result_list.append({
                "segment_id": segment_count,
                "logic": " + ".join(tup),
                "query": " AND ".join(positives)
            })
            segment_count += 1

    return result_list


def generate_query_strings_n_dimensions(dimensions_dict, seed, key_max):
    """
   Given dimensions and associated words, the seg1 seed and the max length of query,
   sets up and generates the query strings dynamically, depending on the number of dimensions.
        Args:
            dimensions_dict: dictionary containing the dimensions data. key=name, value=list of words
            seed: seg1 seed
            key_max: the maximum number of words (32 in Google's case)
        Returns:
            result_data: an object containing data about each of the segments (id, logic, query)
            Returns None if check_length returns False
    """

    dimensions_data = {}
    dimensions = dimensions_dict.keys()

    words_to_exclude = []

    # setup the dimensions data object. Contains:
    # the word list, positive segment and negative segment associated with the dimension
    for name, lis in dimensions_dict.items():
        dimensions_data[name] = {"wordsList": lis, "pos": pos_query_segment(lis), "neg": neg_query_segment(lis)}
        words_to_exclude += lis

    random = get_random_query(words_to_exclude)

    # if the number of keywords is less than the defined max number, don't generate the queries.
    if check_length(seed, random, dimensions_dict.values(), key_max):
        result_data = generate_result_list(dimensions_data, dimensions, seed, random)
        return result_data
    else:
        return {}


def check_length(seed, random, query_words, key_max):
    """
    Google limits searches to 32 words, so we need to make sure we won't be generating anything longer
    Need to consider
    - number of words in seed
    - number of words in random phrase
    - number of words in the lists from the query

    Args:
        seed: the seed for segment 1
        random: the random query string for segment 0
        query_words: object with key=name of dimension, value=list of keywords to use in query
        key_max: the maximum number of words (32 in Google's case)

    Returns:
        bool: True for correct number of words, False for too many

    """
    all_query_words = " ".join(list(itertools.chain.from_iterable(query_words))).split(' ')
    total_words = len(seed.split(" ")) + len(random.split(" ")) + len(all_query_words)

    if total_words <= key_max:
        return True
    else:
        print("The maxiumum number of keywords is:", key_max, "\nYou have:", total_words)
        return False


def main():
    """
        Added for testing
    """
    topic_strings = ["credibility", "assessment"]
    reason_indicators = ["because", "however", "conclude", "for example"]
    experience_indicators = ["i", "our", "experience", "my"]
    people_strings = ["Stefan Hall", "Liz Richardson", "Ash Williams"]
    max_keywords = 32

    three_dimensions = {"topic": topic_strings, "reason": reason_indicators, "experience": experience_indicators}
    four_dimensions = {"topic": topic_strings, "reason": reason_indicators, "experience": experience_indicators,
                       "people": people_strings}

    queries_3_dimensions = generate_query_strings_n_dimensions(three_dimensions, "software", max_keywords)
    queries_4_dimensions = generate_query_strings_n_dimensions(four_dimensions, "software", max_keywords)

    for obj in queries_3_dimensions:
        print(json.dumps(obj, indent=4))

    for obj in queries_4_dimensions:
        print(json.dumps(obj, indent=4))


if __name__ == '__main__':
    main()