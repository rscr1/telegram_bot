import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config  import Config, load_config
from handlers import (add_item_handlers, other_handlers, prime_handlers, 
                    margin_handlers, calculate_price_handlers, show_item_handlers, 
                    add_sale_handlers, edit_item_handlers)


#init logger
logger = logging.getLogger(__name__)


# config function and starting bot
async def main() -> None:
    
    # comfiguration loggition
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    
    # output to console information about bot start
    logger.info('Starting bot')
    
    # load condig to variable config
    config: Config = load_config()

    # initialize the bot and dispatcher
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    dp.include_router(prime_handlers.router)
    dp.include_router(calculate_price_handlers.router)
    dp.include_router(margin_handlers.router)
    dp.include_router(add_item_handlers.router)
    dp.include_router(show_item_handlers.router)
    dp.include_router(add_sale_handlers.router)
    dp.include_router(edit_item_handlers.router)
    dp.include_router(other_handlers.router)
    
    # skip accumulated message and start bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())