from aiogram.dispatcher.filters import Text
# import data_base
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_create import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

admin_ids = [930143697, 580245280]


async def admin_panel(message: types.Message):
    log(message)
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.from_user.id, 'You don`t have enough permissions to access the admin panel.')
        return

    await bot.send_message(message.from_user.id, 'Welcome to the admin panel!')


def log(message):
    print("<!------!>")

    print(datetime.now())
    print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                          message.from_user.last_name,
                                                          str(message.from_user.id), message.text))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands='settings')
