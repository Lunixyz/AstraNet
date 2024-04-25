import discord
import asyncio
from utils.embeds import embed_function
from utils.thread import thread
import json

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

state = {}
last_state = {
    "sessions_logon": "unknown",
    "community": "unknown",
    "matchmaker": "unknown"
}

f = open("config.json")
data = json.load(f)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):

    if user != reaction.message.author:
        return

    if reaction.emoji != "❓":
        return
    
    embed = embed_function(state)

    await reaction.message.reply(embed=embed)
    await reaction.remove(client.user)
    await reaction.remove(user)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.content.lower().startswith("cs caiu"):
        await message.add_reaction("❓")
    
    if message.content.lower().startswith(">status"):
        embed = embed_function(state)
        await message.reply(embed=embed)
        print(data["channel"])

@client.event
async def on_ready():
    print("[AstraNet] Online")
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(thread(client, data["channel"], state, last_state), loop) 

client.run(data["token"])

