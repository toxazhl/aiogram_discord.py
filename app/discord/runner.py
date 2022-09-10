import logging
import os

import discord
from discord.ext import commands

from app.configreader import config


logger = logging.getLogger(__name__)


async def setup() -> commands.Bot:
    bot = commands.Bot(command_prefix=config.discord.prefix, intents=discord.Intents.all())
    return bot


async def run(bot: commands.Bot):
    logger.info(f'Loadins extensions...')

    # Load extensions
    for file in os.listdir("app/discord/extensions"):
        if file.endswith(".py"):
            await bot.load_extension(f"app.discord.extensions.{file[:-3]}")
    
    # Run bot
    async with bot:
        await bot.start(config.discord.token)

