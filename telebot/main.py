import datetime
import logging
import re

from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN
from database import create_collection, filter_data, mongodb

# Configure logging
logging.basicConfig(level=logging.INFO)

# Token
API_TOKEN = TOKEN


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    create_collection()
    await message.reply(
        """Enter you data like: {
        "dt_from":"2022-09-01T00:00:00",
        "dt_upto":"2022-12-31T23:59:00",
        "group_type":"month"
    }"""
    )


@dp.message_handler()
async def get_answer(message: types.Message):
    data = message.text.replace(" ", "")
    dt_from, dt_upto, group_type = format_answer(data)
    if dt_from and dt_upto and group_type:
        result = filter_data(
            from_date=datetime.datetime.fromisoformat(dt_from.group(1)),
            to_date=datetime.datetime.fromisoformat(dt_upto.group(1)),
            collections=mongodb(),
            group_type=group_type.group(1),
        )
        await message.answer(f"{result}")
    else:
        await message.answer(
            """Enter you data like: {
            "dt_from":"2022-09-01T00:00:00",
            "dt_upto":"2022-12-31T23:59:00",
            "group_type":"month"
        }"""
        )


def format_answer(data):
    dt_from = re.search(r'"dt_from":"(.*?)"', data)
    dt_upto = re.search(r'"dt_upto":"(.*?)"', data)
    group_type = re.search(r'"group_type":"(.*?)"', data)

    return dt_from, dt_upto, group_type


if __name__ == "__main__":
    executor.start_polling(dp)
