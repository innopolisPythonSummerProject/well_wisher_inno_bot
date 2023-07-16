from aiogram import types


async def set_default_commands(dp):
    """List of default commands that appears when '/' is typed"""
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start the dialog with the bot"),
            types.BotCommand("start_chat", "Register this chat"),
            types.BotCommand("add_birthday", "Add birthday to the database"),
            types.BotCommand("add_holiday", "Add holiday to the database"),
            types.BotCommand("get_all_birthdays", "Get list of birthdays"),
            types.BotCommand("get_all_holidays", "Get list of holidays"),
            types.BotCommand("get_birthday", "Get birthday by username"),
            types.BotCommand("get_holiday", "Get holiday by its name"),
        ]
    )
