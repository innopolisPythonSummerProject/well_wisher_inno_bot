import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot)
