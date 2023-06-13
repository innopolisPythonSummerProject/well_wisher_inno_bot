from aiogram import types, Dispatcher
from models import ChatTable
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from bot_create import bot

admin_ids = [930143697, 580245280, 1089210807, 362841815]

engine = create_engine('sqlite:///chats.db')
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()


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

    await message.reply('Таблица создана для данного чата.')


async def add_my_birthday(message: types.Message):
    chat_id = message.chat.id

    table_name = f"table_{chat_id}"

    data_from_user = message.text.split(" ")
    print(data_from_user)

    await message.reply(f"You entered: {data_from_user}")

    # Retrieve the table object based on the table name
    # table = Table(table_name, metadata, autoload=True)

    # Create the insert query and execute it
    # insert_query = table.insert().values(data=data, is_birthday=is_birthday, date=date)
    # session.execute(insert_query)
    #
    # # Commit the transaction to save the changes
    # session.commit()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands='settings')
    dp.register_message_handler(start_handler, commands='start')
    dp.register_message_handler(add_my_birthday, commands='add_my_birthday')
