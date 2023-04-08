import datetime

from telebot.database import filter_data
from telebot.tests.answers import day, hour, month


def test_filter_hours(mongo_client):
    start_date = datetime.datetime.fromisoformat("2022-02-01T00:00:00")
    end_date = datetime.datetime.fromisoformat("2022-02-02T00:00:00")

    result = filter_data(
        from_date=start_date,
        to_date=end_date,
        collections=mongo_client,
        group_type="hour",
    )
    assert result == hour


def test_filter_month(mongo_client):
    start_date = datetime.datetime.fromisoformat("2022-09-01T00:00:00")
    end_date = datetime.datetime.fromisoformat("2022-12-31T23:59:00")

    result = filter_data(
        from_date=start_date,
        to_date=end_date,
        collections=mongo_client,
        group_type="month",
    )
    print(result)
    assert result == month


def test_filter_day(mongo_client):
    start_date = datetime.datetime.fromisoformat("2022-10-01T00:00:00")
    end_date = datetime.datetime.fromisoformat("2022-11-30T23:59:00")

    result = filter_data(
        from_date=start_date,
        to_date=end_date,
        collections=mongo_client,
        group_type="day",
    )
    assert result == day
