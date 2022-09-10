import logging
import os

import discord
from discord.ext.commands import Bot


logger = logging.getLogger(__name__)


async def setup(prefix: str) -> Bot:
    bot = Bot(command_prefix=prefix, intents=discord.Intents.all())
    return bot


async def run(bot: Bot, token: str) -> None:
    logger.info(f'Loadins extensions...')

    # Load extensions
    for file in os.listdir("app/discord/extensions"):
        if file.endswith(".py"):
            await bot.load_extension(f"app.discord.extensions.{file[:-3]}")
    
    async with bot:
        await bot.start(token)

