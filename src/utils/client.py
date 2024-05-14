import asyncio
import json
import os
from utils.thread import thread
from utils.handler import handler
from discord.ext import commands


class AstraNet(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        file = open(f"{os.getcwd()}/../config.json")
        data = json.load(file)

        await handler().setup(self)
        print("Connected to Discord.")

        asyncio.ensure_future(thread(self, data["channel"], data["roleid"]).setup())

    def setup(self):
        file = open(f"{os.getcwd()}/../config.json")
        data = json.load(file)
        self.run(data["token"])

