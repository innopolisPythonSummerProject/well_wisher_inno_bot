import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from bot_create import dp
import main_logic


async def on_startup(_):
    logging.info('Bot is starting...')


if __name__ == '__main__':
    logging.basicConfig(filename="logs.txt",
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    storage = MemoryStorage()
    main_logic.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
