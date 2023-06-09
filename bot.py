import asyncio
import locale
import logging

from aiogram import Bot, Dispatcher

from config_data.config import load_config
from handlers import user_handlers, admin_handlers

logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    config = load_config('myenv.env')

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp: Dispatcher = Dispatcher()

    dp.include_router(admin_handlers.admin_router)
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
