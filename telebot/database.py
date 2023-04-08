import datetime
import os
from typing import Dict, List

import bson
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient
from pymongo.collection import Collection

PATH = os.path.normpath("dataset/sample_collection.bson")


def mongodb() -> Collection:
    client = MongoClient("localhost", 27017)
    db = client["my_database"]
    collection = db["salary"]
    return collection


def create_collection() -> None:
    """Populates the database."""
    table = mongodb()
    bson_data = bson_reader()
    table.insert_many(bson_data)


def bson_reader(path: str = PATH) -> List:
    """Reads prepared data"""
    with open(path, "rb") as f:
        bson_data: List = bson.decode_all(f.read())
        return bson_data


def filter_data(
    from_date, to_date, collections, group_type: str
) -> Dict[str, List]:
    """
    A period of time passes and the result is recorded.
    :param from_date: Date from which to start counting
    :param to_date: Date until which to count
    :param collections: Data from the database
    :param group_type: Period
    :return: Dict
    """
    result = {"dataset": [], "labels": []}

    checkpoint, start_position = get_checkpoint(group_type, from_date)
    data, end_data, start_format = get_date_db(
        collections, group_type, from_date, to_date
    )
    value = 0

    for val in data:
        if val["dt"] >= checkpoint:
            result["labels"].append(start_position.isoformat())
            result["dataset"].append(value)

            value = 0
            checkpoint, start_position = get_checkpoint(group_type, checkpoint)

        if val["dt"] > start_position and val["dt"] > to_date:
            if group_type == "hour":
                result["labels"].append(start_position.isoformat())
                result["dataset"].append(value)
                break
        value += val["value"]

    return result


def get_date_db(collections, group_type, from_date, to_date) -> datetime:
    """
    Gets the required period from the database.
    :param collections: Data from the database
    :param group_type: Period
    :param from_date: Date from which to start counting
    :param to_date: Date until which to count
    :return: Datetime
    """
    end_date, start_format = get_checkpoint(group_type, to_date, on=True)

    # Get data from mangodb
    data = collections.find({"dt": {"$gte": from_date, "$lt": end_date}}).sort(
        "dt"
    )
    return data, end_date, start_format


def get_checkpoint(
    group_type: str, time: datetime, on: bool = False
) -> datetime:
    """
    Takes the start of a time span and adds a user-selectable period to it.
    :param group_type: Period
    :param time: Start position
    :param on: Using the parameter for a large data sample
    :return: Datetime
    """
    hour = 1
    day = 24
    month = 1
    if on:
        hour = 2
        day = 36
        month = 2

    if group_type == "hour":
        time_part = time + relativedelta(hours=hour)
    elif group_type == "day":
        time = datetime.datetime(time.year, time.month, time.day)
        time_part = time + relativedelta(hours=day)
    else:
        time = datetime.datetime(time.year, time.month, day=1)
        time_part = time + relativedelta(months=month)
    return time_part, time


if __name__ == "__main__":
    create_collection()

    #  hour
    # start = datetime.datetime.fromisoformat('2022-02-01T00:00:00')
    # end = datetime.datetime.fromisoformat('2022-02-02T00:00:00')

    # day
    # start = datetime.datetime.fromisoformat('2022-10-01T00:00:00')
    # end = datetime.datetime.fromisoformat('2022-11-30T23:59:00')

    # month
    # start = datetime.datetime.fromisoformat('2022-09-01T00:00:00')
    # end = datetime.datetime.fromisoformat('2022-12-31T23:59:00')

    # x = filter_data(
    #     from_date=start, to_date=end,
    #     collections=mongodb(), group_type="month"
    # )
    # print(x)
    # pass
