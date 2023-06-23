import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from app.set_bot_commands import set_default_commands
from bot_create import dp
from app import main_logic


async def on_startup(dp):
    logging.info("Bot is starting...")
    await set_default_commands(dp)


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
