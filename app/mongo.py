import json
import pymongo


class MongoDbDriver:

    def __init__(self, connectionString: str, database: str, collection: str):
        conn = pymongo.MongoClient(connectionString)[database]
        self.__collection = conn[collection]

    def put_data_to_db(self, data: dict) -> None:
        self.__collection.insert_one(data)