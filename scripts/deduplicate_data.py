from coast_search import search
from pymongo import MongoClient
import sys


def getDB(uri, name):
    """ returns a db object """
    try:
        client = MongoClient(uri)
        db = client[name]
    except Exception as e:
        print(e)
        sys.exit()
    else:
        return db

DB_URL = "mongodb://localhost:27017/test_database"
DB_NAME = "jim_hpt"

def exec():

    db = getDB(DB_URL, DB_NAME)
    print("USING DB", DB_URL, DB_NAME)

    results = db.results.find()
    for res in results:

        json = {
            'results': [res['results']]
        }

        deduplicated = search.deduplicate_urls(json)
        res["deduplicated"] = deduplicated
        print(deduplicated)
        db.deduplicated.insert(res)

    # cursor = db.deduplicated.find()
    # for res in cursor:
    #     urls = (res["deduplicated"]['deduplicated_urls'])
    #     links = [x["links"] for x in res["results"]]
    #     flattened = [item for sublist in links for item in sublist]
    #     print("RESULTS FOR", res["_id"], "----------------------------")
    #     for x in urls:
    #         print(x)
    #
    #     print("WOW", len(urls) == len(flattened))



def dedup_all_results():
    db = getDB(DB_URL, DB_NAME)
    results = db.results.find()
    for res in results:
            print(res)


if __name__ == '__main__':
    dedup_all_results()
