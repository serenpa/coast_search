from pymongo import MongoClient
import sys
from _article_extraction import full_extraction


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


def tryExtract(db):
    res = db.to_extract.find_one()
    url = res['url']
    print(url)

    while db.to_extract.find().count() > 0:
        res = db.to_extract.find_one()
        try:
            url = res['url']
            extracted = full_extraction(url)
            print("exctracted", url)
            db.extracted_articles.insert_one(extracted)
        except Exception:
            print("could not extract", url)
            db.cannot_extract.insert_one(res)
        db.to_extract.remove(res)


def main():
    db = getDB(DB_URL, DB_NAME)
    dedup = db.all_deduplications.find()
    result = dedup[0]
    urls = result['deduplicated_urls']

    for url in urls:
        query = {
            "url": url
        }
        url_to_extract = db.to_extract.find_one(query)
        already_extracted = db.extracted_articles.find_one(query)
        could_not_extract = db.cannot_extract.find_one(query)

        if not url_to_extract and not already_extracted and not could_not_extract:
            print("inserting url", url)
            db.to_extract.insert_one({'url': url})
        else:
            print('url already exists', url)

    tryExtract(db)

if __name__ == '__main__':
    DB_URL = "mongodb://localhost:27017/test_database"
    DB_NAME = "jim_hpt"
    main()


# DB_URL = "mongodb://admin:J45m1n31234@cs15078kn.canterbury.ac.nz:27017"
# DB_NAME = "jim_hpt"
