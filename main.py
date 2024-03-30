import discord
import requests
import asyncio

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

#
#   ID do canal do Discord
#       Implementar um JSON com configurações...
#

channel_id = 1156680390015189033

#
#   Estado atual & último
#       Esses dois objetos guardam informações importantes para que o BOT não repita o mesmo estado.
#       Ele lembrará do último estado de X serviço e fará uma comparação para saber se o serviço já
#       estava assim desde a última verificação.
#

state = {}
last_state = {
    "sessions_logon": "unknown",
    "community": "unknown",
    "matchmaker": "unknown",
    "datacenters": "unknown"
}

#   Dicionários de conversão
#       Trocam palavras-chave para traduções
#       dicionário["chave"] = "valor".

status_dictionary = { 
    "unknown": "Sem conexão com a API. ❌",                   
    "normal": "Normal ✅", 
    "surge": "Falhando ⁉️", 
    "delayed": "Lento 🐢", 
    "idle": "Inativo 💤", 
    "offline": "Fora do ar ❌" 
    }
capacity_dictionary = { 
    "unknown": "Sem conexão...", 
    "full": "Cheia", 
    "high": "Alta", 
    "medium": "Média", 
    "low": "Baixa", 
    "offline": "Desligado" 
    }
load_dictionary = { 
    "unknown": "Sem conexão...", 
    "full": "Total", 
    "high": "Alta", 
    "medium": "Média", 
    "low": "Limitada",  
    "idle": "Inativa" 
    }

#   API de status
#       A cada 30 segundos, uma request para a Steam é feita, retornando um JSON
#       Pegamos esse JSON e escolhemos valores específicos (serviços, criador de 
#       partidas...) Retornamos o status (caso não seja "normal") em um canal 
#       específico do Discord.
#

async def get_services():
    while True:

        channel = client.get_channel(channel_id)

        if not channel:
            return
            
            #   Verificações
            #       Caso X serviço não esteja "normal" e não seja igual ao mesmo 
            #       valor de antes, envie uma mensagem no canal Y.

        if state['sessions_logon'] != "normal" and last_state["sessions_logon"] != state['sessions_logon']:
            last_state["sessions_logon"] = state['sessions_logon']
            embed = discord.Embed()

            embed.title="Sessões"
            embed.description=f"A sessão de logon está `{status_dictionary[state['sessions_logon']]}`"
            embed.colour=discord.Color.red()
               
            await channel.send(embed=embed)

        if state['community'] != "normal" and last_state["community"] != state['community']:
            last_state["community"] = state['community']
            embed = discord.Embed()
            
            embed.title="Comunidade"
            embed.description=f"A comunidade está `{status_dictionary[state['community']]}`"
            embed.colour=discord.Color.red()

            await channel.send(embed=embed)

        if state['matchmaker'] != "normal" and last_state["matchmaker"] != state['matchmaker']:
            last_state["matchmaker"] = state['matchmaker']
            embed = discord.Embed()
            
            embed.title="Criador de partidas"
            embed.description=f"O criador de partidas está `{status_dictionary[state['matchmaker']]}`"
            embed.colour=discord.Color.red()

            await channel.send(embed=embed)
        await asyncio.sleep(30)

async def embed_services(): 

    #
    #   Lista com atualizações dos serviços
    #       Essa função fica responsável pela verificação e
    #       atualização do objeto "state", que guarda o status
    #       de cada serviço do Counter-Strike 2.
    #
        
    api = requests.get('https://ares.lunxi.dev/status')
    response = api.json()["data"]["status"]

    sessions_logon = response['services']['SessionsLogon']
    community = response['services']['SteamCommunity']
    matchmaker = response['matchmaker']['scheduler']
    datacenters = response['datacenters']

    state.update({ 
        "sessions_logon": sessions_logon, 
        "community": community, 
        "matchmaker": matchmaker, 
        "datacenters": datacenters 
        })
    await get_services()

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):

    #
    #   Coleta de emojis
    #       Após a reação do BOT ser adicionada na mensagem do usuário,
    #       o BOT irá verificar se é o emoji correto e se a reação foi
    #       do autor da mensagem. Após isso, ele irá enviar uma embed
    #       com a lista dos status dos serviços do Counter-Strike 2.
    #

    if user != reaction.message.author:
        return

    if reaction.emoji != "❓":
        return
    
    embed = discord.Embed()
    embed.title = "Counter-Strike 2 — Serviços"
    embed.description =f"""
    Sessões: `{status_dictionary[state['sessions_logon']]}`
    Comunidade: `{status_dictionary[state['community']]}`
    Criador de partidas: `{status_dictionary[state['matchmaker']]}`
    \nPara invocar essa mensagem, digite `cs caiu`."""

    embed.color = discord.Color.blue()

    await reaction.message.reply(embed=embed)
    await reaction.remove(client.user)
    await reaction.remove(user)
    

@client.event
async def on_message(message: discord.Message):
  if message.author.bot:
    return

  if message.content.startswith("cs caiu"):
    await message.add_reaction("❓")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.content.startswith("cs caiu"):     
        await message.add_reaction("❓")

#
#   Inicialização
#       Após o BOT inicializar, logo chamamos o asyncio para criar uma tarefa assíncrona
#       Essa tarefa assíncrona segura a função de obtenção de dados da API, a cada 30 
#       segundos essa tarefa é cumprida.

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        asyncio.create_task(embed_services())
    except asyncio.CancelledError:
        pass
