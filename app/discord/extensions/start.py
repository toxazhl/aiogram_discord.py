from asyncio.log import logger
import logging

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.bot.user}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Bot(bot))
