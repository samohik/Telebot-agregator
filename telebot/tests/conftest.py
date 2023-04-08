import os

import pytest
from mongomock import MongoClient

from telebot.database import bson_reader


@pytest.fixture(scope="module")
def mongo_client():
    # Connect to the test database on the MongoDB server
    client = MongoClient("localhost", 27017)
    db = client["test_db"]
    collection = db["test_collection"]

    # load data into the collection
    path = os.path.normpath("./telebot/dataset/sample_collection.bson")
    data = bson_reader(path)
    collection.insert_many(data)

    yield collection

    # clean up after the tests
    collection.drop()
    client.close()
