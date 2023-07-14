import os

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

web_app = WebAppInfo(url=os.getenv("WEB_APP_URL"))

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Web App", web_app=web_app)]], resize_keyboard=True
)
