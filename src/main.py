import discord
import asyncio
import json
from dotenv import load_dotenv
from utils.thread import thread
from utils.handler import handler
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix=">")

file = open("../config.json")
data = json.load(file)

#
#   on_ready()
#       Esse evento é responsável pela inicialização do BOT,
#       nele a função de "thread()" é inicializada em uma
#       thread separada da principal para não causar
#       travamentos no código por interromper a thread
#       principal.
#


@client.event
async def on_ready():
    await handler(client)
    print("[AstraNet] Client connected to Discord.")
    await client.tree.sync()
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(
        thread(client, data["channel"], data["roleid"]), loop
    )


client.run(data["token"])
