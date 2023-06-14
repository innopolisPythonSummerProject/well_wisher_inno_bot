from aiogram import types, Dispatcher
from models import ChatTable
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from bot_create import dp

from bot_create import bot

admin_ids = [930143697, 580245280, 1089210807, 362841815]

engine = create_engine('sqlite:///chats.db')
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import create_engine
from sqlalchemy.engine import reflection



async def admin_panel(message: types.Message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.from_user.id, 'You don`t have enough permissions to access the admin panel.')
        return

    await bot.send_message(message.from_user.id, 'Welcome to the admin panel!')


async def start_handler(message: types.Message):
    # Получаем идентификатор чата
    chat_id = message.chat.id

    # Создаем новую таблицу для чата
    chat_table = ChatTable(chat_id)
    chat_table.table.create(bind=engine, checkfirst=True)

    await message.reply('Bot is ready to work!')


async def add_my_birthday(message: types.Message):
    chat_id = message.chat.id

    table_name = f"table_{chat_id}"

    data_from_user = message.text.split(" ")
    print(data_from_user)

    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    user = callback_query.from_user
    date_str = date.strftime("%d/%m")
    print(date_str)
    chat_id = callback_query.message.chat.id

    if selected:
        table_name = 'table_' + str(chat_id)
        # Retrieve the table object based on the table name
        table = Table(table_name, metadata, autoload_with=engine)

        # Create the insert query and execute it
        # columns = table.c
        # for c in columns:
        #     print(c.name, c.type)

        select_query = table.select().where(table.c.data == user.id)
        results = session.execute(select_query).fetchone()
        if results:
            await callback_query.message.answer(
                f'{callback_query.from_user.first_name}`s birthday is rescheduled for {date.strftime("%d/%m")}',
            )
            update_query = (table.update().where(table.c.data == user.id).values(is_birthday=True, date=date))
            session.execute(update_query)

        else:
            await callback_query.message.answer(
                f'{callback_query.from_user.first_name}`s birthday is scheduled for {date.strftime("%d/%m")}',
            )
            insert_query = table.insert().values(data=user.id, is_birthday= True, date=date)
            session.execute(insert_query)

        # Commit the transaction to save the changes
        session.commit()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands='settings')
    dp.register_message_handler(start_handler, commands='start')
    dp.register_message_handler(add_my_birthday, commands='add_my_birthday')
