import asyncio
import logging

from aiohttp import web

from app.configreader import config
from .handlers.fondy import fondy_callback_handler


logger = logging.getLogger(__name__)


async def setup() -> web.Application:
    app = web.Application()
    app.add_routes([
        web.post(config.fondy.webhook_path, fondy_callback_handler),
    ])
    
    return app


async def run(app: web.Application):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=config.webapp.host, port=config.webapp.port)
    await site.start()

    logger.info(f'Running app on {config.webapp.host}:{config.webapp.port}')
    await asyncio.Event().wait()
