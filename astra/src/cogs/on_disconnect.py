from discord.ext import commands
from utils.thread import thread
import asyncio
import json
import os


class Connection(commands.Cog):
    def __init__(self, bot) -> commands.Bot:
        self.bot = bot

    @commands.Cog.listener()
    async def on_disconnect(self):
        print("Disconnected from Discord, waiting for session to resume...")

    @commands.Cog.listener()
    async def on_resumed(self):
        with open(f"{os.getcwd()}/astra/state.json", "r+") as f:
            data = json.load(f)
            print("Session resumed, re-running thread-loop.")
            asyncio.ensure_future(thread(self, data["channel"], data["roleid"]).setup())

async def setup(bot: commands.Bot):
    await bot.add_cog(Connection(bot))
