import json
from bson import json_util

from pymongo import MongoClient
from loguru import logger

from datetime import datetime

SEARCH_FILTERS = {
    # can add a value check (among possible values)
    "institution": lambda x: {"institutions": x},
    "status": lambda x: {"status": x},
    "author": lambda x: {"author": x},
    # can check if before/after are consistent
    "created_at_before": lambda x: {"created_at": {"$lte": datetime.strptime(x, "%Y-%m-%d").isoformat()}},
    "created_at_after": lambda x: {"created_at": {"$gte": datetime.strptime(x, "%Y-%m-%d").isoformat()}},
    "published_at_before": lambda x: {"published_at": {"$lte": datetime.strptime(x, "%Y-%m-%d").isoformat()}},
    "published_at_after": lambda x: {"published_at": {"$gte": datetime.strptime(x, "%Y-%m-%d").isoformat()}},
}

class Mongo:
    def __init__(self):
        logger.info(f"Connecting to MongoDB")
        self.client = MongoClient("mongodb://localhost:27017/") # can be env var
        logger.info(f"Connected to MongoDB")

        if "amendments_db" in self.client.list_database_names():
            logger.info("Connected to database")
        else:
            logger.critical("amendments_db not found")
            raise Exception("amendments_db not found")

        self.database = self.client["amendments_db"]

        if "amendments_coll" in self.database.list_collection_names():
            logger.info("Connected to collection")
        else:
            logger.critical("amendments_coll not found")
            raise Exception("amendments_coll not found")

        self.collection = self.database["amendments_coll"]

    def search(self, keywords: str, filters: dict[str, str] = {}) -> list[str]:
        query = {
            "$and": [
                {"$or": [
                    {"dispositif": {"$regex": keywords}},     # can be advanced regex to match words separately instead
                    {"expose_sommaire": {"$regex": keywords}} # of a single str // currently case and accent sensitive
                ]},
            ] + [
                SEARCH_FILTERS[filter_key](filter_value)
                for filter_key, filter_value in filters.items()
                if filter_key in SEARCH_FILTERS.keys()
            ]
        }
        amendments = json.loads(json_util.dumps({"amendments": [x for x in self.collection.find(query)]}))
        return amendments

    @staticmethod
    def searchError(error: str) -> dict[str, str]:
        return {"error": error}

    def generate_stats(self):
        query = [
            {
                "$group": {
                    "_id": ["$author", "$institution"],
                    "count": {"$sum": 1}
                }
            }
        ]
        stats = json.loads(json_util.dumps({"stats": [x for x in self.collection.aggregate(query)]}))
        return stats

    def search_author(self, author: str) -> dict[str, str]:
        query_amendments = {
            "author": author
        }
        query_stats = [
            {
                "$group": {
                    "_id": "$author",
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {"_id" : author},
            }
        ]
        # should use lookup but lack of time
        amendments = json.loads(json_util.dumps({
            "amendments": [x for x in self.collection.find(query_amendments)],
            "stats": [x for x in self.collection.aggregate(query_stats)]
        }))
        print(amendments)
        return amendments