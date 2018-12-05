"""
    Title: file_utils.py

    Author: Ashley Williams

    Description: A collection of generic utility functions that are used
    throughout coast by various modules relating to reading and writing to
    files.
"""
import sys
import json
from pathlib import Path
from datetime import date


def get_from_file(filename):
    """
        Reads a file and returns each line as a list of strings.

        Notes:
            1. All double quotes are replaced with single quotes.
            2. New line (\n) characters are removed.

        Args:
            filename: The path to the file you wish to read.

        Returns:
            res: A list of strings, where each string is a line in the file.
    """
    ifile = open(filename)
    lines = ifile.readlines()
    ifile.close()

    res = []
    for line in lines:
        res.append(line.replace('"', "'").replace('\n', ''))

    return res


def get_from_file_list(file_list):
    """
    Given a list of file names, reads from each of these and returns a dictionary with filename: list of words
    :param file_list:
    :return:
    """
    res = {}
    # want a dictionary with filename: list of words
    for file in file_list:
        words = get_from_file(file)
        res[Path(file).stem] = words

    return res


def get_json_from_file(filename):
    """
        Reads a JSON file and returns as an object.

        Args:
            filename: The path to the JSON file you wish to read.

        Returns:
            res: A JSON object, generated from the contents of the file.

        Err:
            In the event of an error, the error is printed to the stdout.
    """
    try:
        with open(filename) as ifile:
            res = json.load(ifile)
            return res
    except Exception as e:
        sys.stdout.write(str(e))


def number_of_days_past_start_date(config):
    """
    Gets the day number past the start date defined in the config
    (eg if the start date was a monday and today was a wednedsay the day would be 3
    :param config: config file configs start_date property
    :return: number of days past start date
    """
    start_date_parts = config['start_date'].split('-')
    start_date = date(int(start_date_parts[2]), int(start_date_parts[1]), int(start_date_parts[0]))

    # Get the day - starting from one
    todays_date = date.today()
    days_past_start_date = (todays_date - start_date).days + 1
    return days_past_start_date
