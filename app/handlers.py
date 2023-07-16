"""All handlers within the bot"""

import datetime
import json

import requests
from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from sqlalchemy import String, Table, cast, func, inspect, select

from app.database import engine, metadata, session
from app.keyboard import keyboard
from app.models import ChatTable, Holiday
from creation import bot, dp

holiday = Holiday()

INSPECTOR = inspect(engine)


async def start(message: types.Message):
    """Needed with WebApp interaction"""
    await bot.send_message(
        message.chat.id, "Bot is ready to work!", reply_markup=keyboard
    )


async def get_user_data(user_id):
    """Return data about user based on its id"""
    user = await bot.get_chat(user_id)
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    }
    return user_data


async def start_handler(message: types.Message):
    """Register chat in the database, create a table"""
    # Получаем идентификатор чата
    chat_id = message.chat.id

    # Создаем новую таблицу для чата
    chat_table = ChatTable(chat_id)
    chat_table.table.create(bind=engine, checkfirst=True)

    await message.reply("Bot is ready to work!")


async def add_birthday(message: types.Message):
    """Calls the calendar to specify the date of the birthday"""
    chat_id = message.chat.id

    data_from_user = message.text.split(" ")

    holiday.is_birthday = True

    await message.answer(
        "Please select a date: ", reply_markup=await SimpleCalendar().start_calendar()
    )


async def delete_birthday(message: types.Message):
    """Delete birthday from the database"""
    chat_id = message.chat.id

    table_name = f"table_{chat_id}"
    table = Table(table_name, metadata, autoload_with=engine)

    select_query = table.select().where(table.c.data == message.from_user.id)
    result = session.execute(select_query).fetchone()

    if result:
        await message.answer("Your birthday was successfully deleted")
        # Запись с заданным user.id найдена
        delete_query = table.delete().where(table.c.data == message.from_user.id)

        # Выполните запрос на удаление записи
        session.execute(delete_query)
        session.commit()
    else:
        await message.answer("Sorry, but there is no information about your birthday")


async def get_birthday(message: types.Message):
    """Get birthday date by specifying user`s Telegram alias"""
    data_from_user = message.text.split(" ")
    entered_username = " ".join(data_from_user[1:]).strip()

    if not entered_username:
        await message.answer(
            f"Please, enter /get_birthday username of a person",
        )

    else:
        chat_id = message.chat.id

        table_name = f"table_{chat_id}"
        table = Table(table_name, metadata, autoload_with=engine)

        select_query = table.select().where(table.c.is_birthday == 1)
        results = session.execute(select_query).fetchall()

        user_found = False
        for row in results:
            user_data = await get_user_data(row[0])
            if user_data["username"] == entered_username:
                user_found = True
                correct_date = str(row[2]).split()[0].split("-")

                await message.answer(
                    f"{correct_date[2]}.{correct_date[1]}",
                )
                break

        if not user_found:
            await message.answer(
                f"There is no information about birthday of this person",
            )


async def get_all_birthdays(message: types.Message):
    """Get list of all birthdays"""
    chat_id = message.chat.id

    table_name = f"table_{chat_id}"
    table = Table(table_name, metadata, autoload_with=engine)

    select_query = table.select().where(table.c.is_birthday == 1)
    results = session.execute(select_query).fetchall()

    answer_data = ""
    for row in results:
        print(row)
        user_data = await get_user_data(row[0])
        correct_date = str(row[2]).split()[0].split("-")
        answer_data += f'@{user_data["username"]} {correct_date[2]}.{correct_date[1]}\n'

    await message.answer(
        answer_data,
    )


async def get_all_holidays(message: types.Message):
    """Get list of all holidays"""
    chat_id = message.chat.id

    table_name = f"table_{chat_id}"
    table = Table(table_name, metadata, autoload_with=engine)

    select_query = table.select().where(table.c.is_birthday == 0)
    results = session.execute(select_query).fetchall()

    answer_data = ""
    for row in results:
        correct_date = str(row[2]).split()[0].split("-")
        answer_data += f"{row[0]} {correct_date[2]}.{correct_date[1]}\n"

    await message.answer(
        answer_data,
    )


async def get_holiday(message: types.Message):
    """Get holiday by its name"""
    data_from_user = message.text.split(" ")
    entered_holiday = " ".join(data_from_user[1:]).strip()

    if not entered_holiday:
        await message.answer(
            f"Please, enter /get_birthday name of a holiday",
        )

    else:
        chat_id = message.chat.id

        table_name = f"table_{chat_id}"
        table = Table(table_name, metadata, autoload_with=engine)

        select_query = table.select().where(table.c.is_birthday == 0)
        results = session.execute(select_query).fetchall()

        hd_found = False
        for row in results:
            print(row)
            if row[0] == entered_holiday:
                hd_found = True
                correct_date = str(row[2]).split()[0].split("-")

                await message.answer(
                    f"{correct_date[2]}.{correct_date[1]}",
                )
                break

        if not hd_found:
            await message.answer(
                f"There is no information about this holiday",
            )


async def add_holiday(message: types.Message):
    """Calls the calendar to specify the date of the holiday"""
    data_from_user = message.text.split(" ")
    print(data_from_user)

    holiday.is_birthday = False
    holiday.holiday_name = " ".join(data_from_user[1:])

    if not holiday.holiday_name.strip():
        await message.answer(
            f"Please, enter /add_holiday name of holiday",
        )
    else:
        await message.answer(
            "Please select a date: ",
            reply_markup=await SimpleCalendar().start_calendar(),
        )


async def delete_holiday(message: types.Message):

    data_from_user = message.text.split(" ")
    holiday_name = " ".join(data_from_user[1:])

    if not holiday_name.strip():
        await message.answer(
            f"Please, enter /delete_holiday name of holiday",
        )
    else:
        chat_id = message.chat.id

        table_name = f"table_{chat_id}"
        table = Table(table_name, metadata, autoload_with=engine)

        select_query = table.select().where(table.c.data == holiday_name)
        result = session.execute(select_query).fetchone()

        if result:
            await message.answer(f"{holiday_name} was successfully deleted")

            delete_query = table.delete().where(table.c.data == holiday_name)

            session.execute(delete_query)
            session.commit()
        else:
            await message.answer(
                "Sorry, but there is no information about this holiday"
            )


async def get_today(message: types.Message):
    data_from_user = message.text.split(" ")
    print(data_from_user)

    chat_id = message.chat.id

    table_name = f"table_{chat_id}"
    table = Table(table_name, metadata, autoload_with=engine)

    print(datetime.date.today().strftime("%Y-%m-%d"))

    # select_query = table.select().where(func.split(table.c.date, ' ')[0] == datetime.date.today().strftime('%Y-%m-%d'))

    date_str = datetime.date.today().strftime("%Y-%m-%d")
    substr_date = func.substr(table.c.date, 1, func.instr(table.c.date, " ") - 1).label(
        "substr_date"
    )
    select_query = table.select().where(cast(substr_date, String).like(f"{date_str}%"))

    results = session.execute(select_query).fetchall()

    hd_found = False
    answer_data = "Today`s events:\n"
    for row in results:
        if row[1] == "0":
            hd_found = True
            answer_data += f"{row[0]}\n"
        else:
            hd_found = True
            user_data = await get_user_data(row[0])
            answer_data += f'{user_data["username"]}`s birthday\n'

    if not hd_found:
        await message.answer(
            f"There are no any holidays today :(",
        )
    else:
        await message.answer(
            answer_data,
        )


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    """Utility function to run the calendar"""
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    user = callback_query.from_user
    chat_id = callback_query.message.chat.id

    if selected:
        if holiday.is_birthday is True:
            await add_birthday_to_db(
                chat_id=chat_id, user=user, callback_query=callback_query, date=date
            )
        else:
            await add_holiday_to_db(
                chat_id=chat_id,
                holiday_name=holiday.holiday_name,
                callback_query=callback_query,
                date=date,
            )


async def add_birthday_to_db(chat_id, user, callback_query, date):
    """Process adding birthday in the database"""
    table_name = "table_" + str(chat_id)
    # Retrieve the table object based on the table name
    table = Table(table_name, metadata, autoload_with=engine)

    select_query = table.select().where(table.c.data == user.id)
    results = session.execute(select_query).fetchone()
    if results:
        await callback_query.message.answer(
            f'{callback_query.from_user.first_name}`s birthday is rescheduled for {date.strftime("%d/%m")}',
        )
        update_query = (
            table.update()
            .where(table.c.data == user.id)
            .values(is_birthday=True, date=date)
        )
        session.execute(update_query)

    else:
        await callback_query.message.answer(
            f'{callback_query.from_user.first_name}`s birthday is scheduled for {date.strftime("%d/%m")}',
        )
        insert_query = table.insert().values(data=user.id, is_birthday=True, date=date)
        session.execute(insert_query)

    session.commit()


async def add_holiday_to_db(chat_id, holiday_name, callback_query, date):
    """Process adding holiday in the database"""
    table_name = "table_" + str(chat_id)
    table = Table(table_name, metadata, autoload_with=engine)

    select_query = table.select().where(table.c.data == holiday_name)
    results = session.execute(select_query).fetchone()
    if results:
        await callback_query.message.answer(
            f'{holiday_name} is rescheduled for {date.strftime("%d/%m")}',
        )
        update_query = (
            table.update()
            .where(table.c.data == holiday_name)
            .values(is_birthday=False, date=date)
        )
        session.execute(update_query)

    else:
        await callback_query.message.answer(
            f'{holiday_name} is scheduled for {date.strftime("%d/%m")}',
        )
        insert_query = table.insert().values(
            data=holiday_name, is_birthday=False, date=date
        )
        session.execute(insert_query)

    session.commit()


def set_connection_and_return_args():
    """Connect with the special API that generates image_url and text"""
    image_params = {"kitty": "True", "Sparkles": "False"}
    image_request = requests.get(
        "https://well-wisher.onrender.com/image?prompt=holiday&kitty=true&Sparkles=true",
        params=image_params,
    )
    text_params = {"holiday": "birthday"}
    text_request = requests.get(
        "https://well-wisher.onrender.com/greeting?holiday=birthday",
        params=text_params,
    )
    random_text = text_request.text
    random_image_url = image_request.text

    response_data_text = json.loads(random_text)
    response_data_image = json.loads(random_image_url)

    return response_data_text, response_data_image


async def send_birthday_congratulations():
    """Send birthday congratulation in the chat"""
    today = ".".join(str(datetime.date.today()).split("-")[1:])

    tables = INSPECTOR.get_table_names()

    for table_name in tables:
        if table_name.startswith("table_"):
            table = Table(table_name, metadata, autoload_with=engine)

            select_query = select(table)

            result = session.execute(select_query)

            rows = result.fetchall()

            for row in rows:
                date = ".".join(row[2].split()[0].split("-")[1:])
                if date == today:
                    if row[1] == "1":
                        chat_id = int(table_name.split("_")[1])
                        user_data = await get_user_data(row[0])
                        holiday_message = (
                            f"Happy birthday, @{user_data['username']}! 🎉🎂"
                        )

                        (
                            response_data_text,
                            response_data_image,
                        ) = set_connection_and_return_args()

                        random_image_url = response_data_image["data"][0]["url"]

                        random_text = response_data_text["choices"][0]["text"]

                        random_image_hyperlink = (
                            f"[Link to the picture^]({random_image_url})"
                        )

                        total_congratulation = (
                                holiday_message
                                + "\n"
                                + random_text
                                + "\n"
                                + "\n"
                                + random_image_hyperlink
                        )
                        await bot.send_message(
                            chat_id, total_congratulation, parse_mode="Markdown"
                        )

                    elif row[1] == "0":
                        chat_id = int(table_name.split("_")[1])
                        holiday_message = f"Today is {row[0]}!"

                        await bot.send_message(chat_id, holiday_message)


@dp.message_handler(content_types="web_app_data")
async def get_data(web_app_message):
    """Get sent data from WebApp"""
    data = web_app_message["web_app_data"]["data"]
    data_json = json.loads(data)
    image_url = data_json["picture_src"]
    text = data_json["text_content"]

    image_hyperlink = f"[Link to the picture^]({image_url})"

    total_congratulation = text + "\n" + image_hyperlink

    await bot.send_message(
        chat_id=web_app_message.chat.id,
        text=total_congratulation,
        parse_mode="Markdown",
    )


def register_handlers(dp: Dispatcher):
    """The list of all handlers"""
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(start_handler, commands="start_chat")
    dp.register_message_handler(add_birthday, commands="add_birthday")
    dp.register_message_handler(add_holiday, commands="add_holiday")
    dp.register_message_handler(delete_birthday, commands="delete_birthday")
    dp.register_message_handler(delete_holiday, commands="delete_holiday")
    dp.register_message_handler(get_all_birthdays, commands="get_all_birthdays")
    dp.register_message_handler(get_all_holidays, commands="get_all_holidays")
    dp.register_message_handler(get_birthday, commands="get_birthday")
    dp.register_message_handler(get_holiday, commands="get_holiday")
    dp.register_message_handler(get_today, commands="get_today")
