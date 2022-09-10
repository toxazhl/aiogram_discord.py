import logging

from aiohttp import web
from aiohttp.web_request import Request
from aiogram import Bot, Dispatcher
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from app.configreader import config
from app.db import queries


logger = logging.getLogger(__name__)


async def fondy_callback_handler(request: Request):
    telegram_bot: Bot = request.app['telegram_bot']
    dp: Dispatcher = request.app['dp']
    discord_bot: commands.Bot = request.app['discord_bot']
    db_pool: sessionmaker = request.app['db_pool']

    # TODO payment processing
    
    payment_data = await request.json()
    logger.debug(f'Fondy request: {payment_data}')

    logger.info(f'Payment {payment_data["payment_id"]} is {payment_data["order_status"]}')

    order_status = payment_data['order_status']

    if order_status == 'approved':
        pass

    elif order_status == 'declined':
        pass

    elif order_status == 'reversed':  
        pass

    elif order_status == 'expired':
        pass

    else:
        pass

    return web.json_response({"status": "OK"}, status=200)
