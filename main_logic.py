from aiogram.dispatcher.filters import Text
# import data_base
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_create import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

import logging

admin_ids = [930143697, 580245280, 1089210807, 362841815]


async def admin_panel(message: types.Message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.from_user.id, 'You don`t have enough permissions to access the admin panel.')
        return

    await bot.send_message(message.from_user.id, 'Welcome to the admin panel!')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands='settings')
