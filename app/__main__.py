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


def setup_logging():
    # Open logging config file
    with open('app/logging.yaml', 'r') as stream:
        logging_config = yaml.load(stream, Loader=yaml.FullLoader)

    # Create log directories if not exists
    for handler in logging_config['handlers'].values():
        if log_filename := handler.get('filename'):
            os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    # Configure logging
    logging.config.dictConfig(logging_config)


async def main():
    # Configure logging
    setup_logging()

    logger.info('Starting...')
    
    coroutines = []
    
    # Creating DB engine for PostgreSQL
    engine = create_async_engine(config.storages.postgres_dsn, future=True, echo=False)

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # Creating Fondy client
    fondy_client = FondyClient(config.fondy.merchant_id, config.fondy.secret_key)
    
    # Creating telegram bot
    telegram_bot, dp = await telegram.setup(db_pool)

    # Creating discord bot
    discord_bot = await discord.setup()

    coroutines.append(discord.run(discord_bot))

    # Custom data for telegram handlers
    custom_data = {
        'fondy': fondy_client,
    }

    # Run webhook if enabled
    if config.webhook.enable:
        # Creating web app
        app = await web_app.setup()

        app['telegram_bot'] = telegram_bot
        app['discord_bot'] = telegram_bot
        app['dp'] = dp
        app['fondy'] = fondy_client
        app['db_pool'] = db_pool

        # Setting up webhook
        await telegram.setup_webhook(telegram_bot, dp, app, **custom_data)

        # Running web app
        coroutines.append(web_app.run(app))

        #await web_app.run(app)
    
    else:
        # Running bot
        coroutines.append(telegram.run(telegram_bot, dp, **custom_data))

        # await telegram.run(bot, dp, **custom_data)
    
    await asyncio.gather(*coroutines)

    
if __name__ == '__main__':
    asyncio.run(main())
