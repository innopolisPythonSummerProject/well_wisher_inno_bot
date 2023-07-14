from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from creation import web_app

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Web App", web_app=web_app)]], resize_keyboard=True
)
