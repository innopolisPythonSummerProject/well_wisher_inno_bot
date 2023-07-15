import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import find_dotenv, load_dotenv

from app import handlers
from app.handlers import send_birthday_congratulations
from app.set_bot_commands import set_default_commands
from creation import dp

load_dotenv(find_dotenv())


async def on_startup(dp):
    logging.info("Bot is starting...")
    await set_default_commands(dp)

    # Send the keyboard to the user
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_birthday_congratulations, "interval", day=1)
    scheduler.start()


if __name__ == "__main__":
    logging.basicConfig(
        filename="middleware/logs.txt",
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    storage = MemoryStorage()
    handlers.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
