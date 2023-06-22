import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from app import main_logic
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot)


async def on_startup(_):
    logging.info("Bot is starting...")


if __name__ == "__main__":
    logging.basicConfig(
        filename="middleware/logs.txt",
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    storage = MemoryStorage()
    main_logic.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
