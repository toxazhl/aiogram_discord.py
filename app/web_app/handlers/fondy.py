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

    async def payment_approved(payment_id, order_id, order_status, rectoken, rectoken_lifetime, **kwargs):
        pass

    async def payment_declined(payment_id, order_status, **kwargs):
        pass

    async def payment_reversed(payment_id, order_status, **kwargs):
        pass

    async def payment_expired(payment_id, order_status, **kwargs):
        pass

    async def payment_update_status(payment_id, order_status, **kwargs):
        pass

    
    payment_data = await request.json()
    logger.debug(f'Fondy request: {payment_data}')

    logger.info(f'Payment {payment_data["payment_id"]} is {payment_data["order_status"]}')

    match payment_data['order_status']:
        case 'approved':
            await payment_approved(**payment_data)
        case 'declined':
            await payment_declined(**payment_data)
        case 'reversed':
            await payment_reversed(**payment_data)
        case 'expired':
            await payment_expired(**payment_data)
        case _:
            await payment_update_status(**payment_data)

    return web.json_response({"status": "OK"}, status=200)
