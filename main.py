import discord
import asyncio
import json
from utils.embeds import embed_function
from utils.thread import thread

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

f = open("config.json")

data = json.load(f)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):

    if user != reaction.message.author:
        return

    if reaction.emoji != "❓":
        return

    await reaction.message.reply(embed=embed_function())
    await reaction.remove(client.user)
    await reaction.remove(user)
    

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.content.lower().startswith("cs caiu"):
        await message.add_reaction("❓")
    
    if message.content.lower().startswith(">status"):
        await message.reply(embed=embed_function())
        print(data["channel"])


@client.event
async def on_ready():
    print("[AstraNet] Online")
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(thread(client, data["channel"], data["roleid"]), loop)

client.run(data["token"])

