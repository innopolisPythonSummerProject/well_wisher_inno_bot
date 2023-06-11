import logging

from aiogram.utils import executor
from bot_create import dp
import main_logic


async def on_startup(_):
    logging.info('Bot is starting...')
    # data_base.sql_start()


if __name__ == '__main__':
    logging.basicConfig(filename="logs.txt",
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    main_logic.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
