import logging
import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram.utils import executor

from app.set_bot_commands import set_default_commands
from bot_create import dp
from app import main_logic
from bot_create import bot

from dotenv import load_dotenv, find_dotenv
from app.main_logic import run_infinity_loop

load_dotenv(find_dotenv())


async def on_startup(dp):
    logging.info("Bot is starting...")
    await set_default_commands(dp)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Menu", web_app=WebAppInfo(url=os.getenv("WEB_APP_URL")))
    )


if __name__ == "__main__":
    logging.basicConfig(
        filename="middleware/logs.txt",
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    storage = MemoryStorage()
    main_logic.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

