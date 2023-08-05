# -*- coding: utf-8 -*-
from pymongo import MongoClient

DEFAULT_HOST = {
    "host": "localhost",
    "port": 27017
}


def from_mongo(db_name: str, col_name: str, host: dict = None):
    if host is None:
        host = DEFAULT_HOST
    client = MongoClient(**host)
    return client[db_name][col_name].find({}, {"_id": 0})
