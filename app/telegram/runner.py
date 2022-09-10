import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from magic_filter import F

from app.configreader import config
from .handlers import setup_routers
from .middlewares.db import DbSessionMiddleware


logger = logging.getLogger(__name__)


async def setup(db_pool) -> tuple[Bot, Dispatcher]:
    # Creating bot and its dispatcher
    bot = Bot(token=config.telegram.token, parse_mode="HTML")

    # Choosing FSM storage
    if config.telegram.fsm_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        dp = Dispatcher(storage=RedisStorage.from_url(config.storages.redis_dsn))
    
    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type == "private")
    
    # Registering middlewares
    dp.update.middleware(DbSessionMiddleware(db_pool))

    # Register handlers
    router = setup_routers()
    dp.include_router(router)

    return bot, dp


async def setup_webhook(
    bot: Bot, dp: Dispatcher, app: web.Application, **data
) -> None:
    me = await bot.get_me()
    url = f'{config.webhook.domain}{config.telegram.webhook_path}'
    logger.info(f'Run webhook for bot @{me.username} id={bot.id} - \'{me.full_name}\' on {url}')

    # Set webhook
    await bot.set_webhook(
        url=url,
        drop_pending_updates=True,
        allowed_updates=dp.resolve_used_update_types()
    )

    # Registering webhook handler for bot
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        **data
    ).register(app, path=config.telegram.webhook_path)
    

async def run(bot: Bot, dp: Dispatcher, **data) -> None:
    # Delete webhook
    await bot.delete_webhook()

    # Start polling
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **data
    )
    
