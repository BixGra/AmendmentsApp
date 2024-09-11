import json
from pymongo import MongoClient
from loguru import logger

def initialize() -> None:
    logger.info("Connecting to MongoDB")
    client = MongoClient("mongodb://localhost:27017/") # can be env var
    logger.info("Connected to MongoDB")

    logger.info("Creating database")
    if "amendments_db" in client.list_database_names():
        logger.info("Database already exists")
        logger.info("Dropping database")
        client.drop_database("amendments_db")
        logger.info("Database dropped")
    database = client["amendments_db"]
    logger.info("Database created")

    logger.info("Creating collection")
    if "amendments_collection" in database.list_collection_names():
        logger.info("Collection already exists")
        logger.info("Dropping collection")
        database.drop_collection("amendments_collection")
        logger.info("Collection dropped")
    collection = database["amendments_coll"]
    logger.info("Collection created")

    logger.info("Loading JSON")
    with open("./src/init/amendment_data_set.json", "r") as file:
        data = json.load(file)
    logger.info("Loaded JSON")

    to_insert_size = len(data)
    logger.info(f"Entries to insert into the collection : {to_insert_size}")

    logger.info("Inserting data into collection")
    collection.insert_many(data)
    logger.info("Data inserted into collection")

    inserted_size = len(list(collection.find()))
    logger.info(f"Entries in the collection : {inserted_size} - ({inserted_size/to_insert_size*100:.2f}% success)")

if __name__ == "__main__":
    initialize()
