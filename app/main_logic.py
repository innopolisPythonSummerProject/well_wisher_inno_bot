import asyncio

from aiogram import types, Dispatcher
from app.models import ChatTable
from sqlalchemy import create_engine, MetaData, Table, func, cast, String
from sqlalchemy.orm import sessionmaker
import datetime

# from app.commands import set_default_commands

from aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram.types import CallbackQuery
from bot_create import dp

from bot_create import bot
from app.models import Holiday

admin_ids = [930143697, 580245280, 1089210807, 362841815]

engine = create_engine("sqlite:///chats.db")
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()
holiday = Holiday()


async def admin_panel(message: types.Message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.from_user.id, 'You don`t have enough permissions to access the admin panel.')
        return

    await bot.send_message(message.from_user.id, 'Welcome to the admin panel!')


async def get_user_data(user_id):
    user = await bot.get_chat(user_id)
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    }
    return user_data


async def start_handler(message: types.Message):
    schedule_time = datetime.time(hour=11, minute=26)
    await schedule_task(schedule_time, send_birthday_congratulations)

    # Получаем идентификатор чата
    chat_id = message.chat.id

    # Создаем новую таблицу для чата
    chat_table = ChatTable(chat_id)
    chat_table.table.create(bind=engine, checkfirst=True)

    await message.reply("Bot is ready to work!")


async def add_birthday(message: types.Message):
    chat_id = message.chat.id

    data_from_user = message.text.split(" ")
    print(data_from_user)

    holiday.is_birthday = True

    await message.answer(
        "Please select a date: ", reply_markup=await SimpleCalendar().start_calendar()
    )


async def delete_birthday(message: types.Message):
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
    data_from_user = message.text.split(" ")
    print(data_from_user)
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
    data_from_user = message.text.split(" ")
    print(data_from_user)
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
    print(data_from_user)

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

    print(datetime.date.today().strftime('%Y-%m-%d'))

    # select_query = table.select().where(func.split(table.c.date, ' ')[0] == datetime.date.today().strftime('%Y-%m-%d'))

    date_str = datetime.date.today().strftime('%Y-%m-%d')
    substr_date = func.substr(table.c.date, 1, func.instr(table.c.date, ' ') - 1).label('substr_date')
    select_query = table.select().where(cast(substr_date, String).like(f'{date_str}%'))


    results = session.execute(select_query).fetchall()


    hd_found = False
    answer_data = 'Today`s events:\n'
    for row in results:
        if row[1]=='0':
            hd_found=True
            answer_data += f'{row[0]}\n'
        else:
            hd_found=True
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
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    user = callback_query.from_user
    # date_str = date.strftime("%d/%m")
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


async def schedule_task(schedule_time, callback):
    print('schedule_task')
    while True:
        now = datetime.datetime.now()
        schedule_time = now.replace(hour=11, minute=26, second=0, microsecond=0)
        if now >= schedule_time:
            # Calculate the next day's schedule time
            next_day = now + datetime.timedelta(days=1)
            next_schedule_time = next_day.replace(hour=11, minute=26, second=0, microsecond=0)
            time_difference = (next_schedule_time - now).total_seconds()

            # Run the task
            await callback()

            # Wait until the next day to schedule the task again
            await asyncio.sleep(time_difference)
        else:
            # Wait for 1 minute and check again
            await asyncio.sleep(60)

async def send_birthday_congratulations():
    today = datetime.date.today()
    tables = metadata.tables.keys()

    for table_name in tables:
        if table_name.startswith("table_"):
            table = Table(table_name, metadata, autoload=True)
            query = table.select().where(func.split(table.c.date, ' ')[0] == today.strftime('%Y-%m-%d'))
            result = await engine.execute(query)
            rows = await result.fetchall()

            for row in rows:
                chat_id = int(table_name.split("_")[1])
                user_name = row.username
                message = f"Happy birthday, {user_name}! 🎉🎂"
                await bot.send_message(chat_id, message)


@dp.message_handler(commands=['fetch_data'])
async def fetch_data_handler(message: types.Message):
    users = session.query().all()
    print(users)
    for user in users:
        # Perform your desired actions with the user data
        user_id = user.id
        user_name = user.name
        await message.answer(f"User ID: {user_id}, Name: {user_name}")


def register_handlers(dp: Dispatcher):
    # dp.register_message_handler(admin_panel, commands='settings')
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(add_birthday, commands="add_birthday")
    dp.register_message_handler(add_holiday, commands="add_holiday")
    dp.register_message_handler(delete_birthday, commands="delete_birthday")
    dp.register_message_handler(delete_holiday, commands="delete_holiday")
    dp.register_message_handler(get_all_birthdays, commands="get_all_birthdays")
    dp.register_message_handler(get_all_holidays, commands="get_all_holidays")
    dp.register_message_handler(get_birthday, commands="get_birthday")
    dp.register_message_handler(get_holiday, commands="get_holiday")
    dp.register_message_handler(get_today, commands="get_today")
