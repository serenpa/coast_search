"""["search_engines"]
    Title: db_utils.py

    Author: Ashley Williams

    Description: A collection of generic utility functions that are used
    throughout coast by various modules relating to the database.
"""
import sys
from pymongo import MongoClient


def get_db(db_url, db_client):
    """
        Given the url and client (db) for a MongoDB, will return a DB object.

        Args:
            db_url: The url of the MongoDB
            db_client: The name of the specific Mongo client to use.

        Returns:
            db: A pymongo database object that allows interaction between
                python and MongoDB

        Err:
            In the event of an error, the error is printed to the stdout and
            program execution is halted.


    """
    try:
        client = MongoClient(db_url)
        db = client[db_client]
    except Exception as e:
        sys.stdout.write(str(e))
        sys.exit()
    else:
        return db


def clean_db(db, collections):
    """
        Will drop each collection in a given list from a given db object.

        Args:
            db: The database object to be cleaned.
            collections: A list of collections to be dropped.

        Returns:
            flag: True if all have been successfully dropped. Else False.

        Err:
            In the event of an error, the error is printed to the stdout.
    """
    flag = True
    for collection in collections:
        try:
            db[collection].drop()
        except Exception as e:
            sys.stdout.write(str(e))
            flag = False

    return flag
