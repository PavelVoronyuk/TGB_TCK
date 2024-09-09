import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config.config import load_config, Config
from handlers import user_handlers, form_fill


logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, parsemode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(user_handlers.user_router, form_fill.form_fill_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
