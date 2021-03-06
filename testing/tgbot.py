import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import databaseHandler

import echo_handler

counter = databaseHandler.sheetRows()

bot_id = 742596099
API_TOKEN = '5465574210:AAHmn0cQlDJNSCROnbHnRLQ7JvixZofw4UQ'
logging.basicConfig(level=logging.INFO)



bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def start_bot():
    echo_handler.setup(dp)

    executor.start_polling(dp, skip_updates=True)

def stop_bot():
    executor.start_polling(dp)
