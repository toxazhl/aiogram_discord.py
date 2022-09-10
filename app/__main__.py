import asyncio
import logging.config
import os
import yaml

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import telegram, web_app, discord
from app.configreader import config
from app.payments import FondyClient


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    with open('app/logging.yaml', 'r') as stream:
        logging_config = yaml.load(stream, Loader=yaml.FullLoader)

    # Create log directories if not exists
    for handler in logging_config['handlers'].values():
        if log_filename := handler.get('filename'):
            os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    logging.config.dictConfig(logging_config)


async def main() -> None:
    setup_logging()

    logger.info('Starting...')
    
    coroutines = []
    
    engine = create_async_engine(config.storages.postgres_dsn, future=True, echo=False)

    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    fondy_client = FondyClient(config.fondy.merchant_id, config.fondy.secret_key)
    
    telegram_bot, dp = await telegram.setup(db_pool)

    discord_bot = await discord.setup()

    coroutines.append(discord.run(discord_bot))

    # Custom data for telegram handlers
    custom_data = {
        'fondy': fondy_client,
    }

    if config.webhook.enable:
        app = await web_app.setup()

        app['telegram_bot'] = telegram_bot
        app['discord_bot'] = telegram_bot
        app['dp'] = dp
        app['fondy'] = fondy_client
        app['db_pool'] = db_pool

        await telegram.setup_webhook(telegram_bot, dp, app, **custom_data)

        coroutines.append(web_app.run(app))
    
    else:
        coroutines.append(telegram.run(telegram_bot, dp, **custom_data))
    
    await asyncio.gather(*coroutines)

    
if __name__ == '__main__':
    asyncio.run(main())
