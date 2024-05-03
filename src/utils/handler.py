import os
from discord.ext import commands


async def handler(client: commands.Bot):
    for file in os.listdir(f"{os.getcwd}/../cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            await client.load_extension(f"cogs.{name}")
