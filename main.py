import discord
import asyncio
import json
from utils.embeds import embed_function
from utils.thread import thread

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

#
#   Abrindo o JSON
#       O arquivo "config.json" é aberto para utilizar os valores de
#       "token", "role_id" e "channel" para suas respectivas funções
#

f = open("config.json")
data = json.load(f)

#
#   on_reaction_add(reaction, user)
#       Esse evento é responsável por responder quando o usuário clicar
#       na reação que o BOT colocou na mensagem do mesmo. Logo após isso
#       ele irá rodar a função "embed_function()"
#

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):

    if user != reaction.message.author:
        return

    if reaction.emoji != "❓":
        return

    await reaction.message.reply(embed=embed_function())
    await reaction.remove(client.user)
    await reaction.remove(user)
    

#
#   on_message(message)
#       Esse evento é responsável por verificar se uma mensagem enviada
#       no Discord começa com "cs caiu" ou "status" e roda as respecti-
#       vas funções.
#
#       No caso do "cs caiu", o BOT irá adicionar uma reação na mensagem
#       e espera que o usuário reaja para continuar. 
#       (veja "on_reaction_add()")
#

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.content.lower().startswith("cs caiu"):
        await message.add_reaction("❓")
    
    if message.content.lower().startswith(">status"):
        await message.reply(embed=embed_function())
        print(data["channel"])

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
    print("[AstraNet] Online")
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(thread(client, data["channel"], data["roleid"]), loop)

client.run(data["token"])

