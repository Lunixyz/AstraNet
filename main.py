import discord
import requests
import asyncio
import threading
import time
import os

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

#
#   ID do canal do Discord
#       Implementar um JSON com configurações...
#

channel_id = 733465378360918066

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
    "matchmaker": "unknown"
}

#   Dicionários de conversão
#       Trocam palavras-chave para traduções
#       dicionário["chave"] = "valor".

status_dictionary = { 
    "unknown": "Sem conexão com a API. ❌",                   
    "normal": "Normal ✅", 
    "surge": "Falhando ⁉️", 
    "delayed": "Lento(a) 🐢", 
    "idle": "Inativo(a) 💤", 
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
api_status_dictionary = {
    200: "OK",
    400: "Bad Request",
    500: "Internal Server Error!!"
}

#   API de status
#       A cada 30 segundos, uma request para a Steam é feita, retornando um JSON
#       Pegamos esse JSON e escolhemos valores específicos (serviços, criador de 
#       partidas...) Retornamos o status (caso não seja "normal") em um canal 
#       específico do Discord.
#

async def get_services():
    channel = client.get_channel(channel_id)
    embed = discord.Embed()


    if not channel:
        return
            
            #   Verificações
            #       Caso X serviço não esteja "normal" e não seja igual ao mesmo 
            #       valor de antes, envie uma mensagem no canal Y.

    content = "# Status do Counter-Strike! :warning:"
    
    if state['sessions_logon'] != "normal" and last_state["sessions_logon"] != state['sessions_logon']:
        last_state["sessions_logon"] = state['sessions_logon']
        print(f"[Sessions] {state['sessions_logon']}")
        embed.title="Sessões"
        embed.description=f"A sessão de logon está `{status_dictionary[state['sessions_logon']]}`"
        embed.colour=discord.Color.red()
        return await channel.send(content=content, embed=embed)
               

    if state['community'] != "normal" and last_state["community"] != state['community']:
        last_state["community"] = state['community']
        print(f"[Community] {state['community']}")
        embed.title="Comunidade"
        embed.description=f"A comunidade está `{status_dictionary[state['community']]}`"
        embed.colour=discord.Color.red()
        return await channel.send(content=content, embed=embed)


    if state['matchmaker'] != "normal" and last_state["matchmaker"] != state['matchmaker']:
        last_state["matchmaker"] = state['matchmaker']
        print(f"[Matchmaker] {state['matchmaker']}")
        embed.title="Criador de partidas"
        embed.description=f"O criador de partidas está `{status_dictionary[state['matchmaker']]}`"
        embed.colour=discord.Color.red()
        return await channel.send(content=content, embed=embed)
    
    print(f"[Sessions] {state['sessions_logon']}")
    print(f"[Community] {state['community']}")
    print(f"[Matchmaker] {state['matchmaker']}")

async def embed_services(): 

    #
    #   Lista com atualizações dos serviços
    #       Essa função fica responsável pela verificação e
    #       atualização do objeto "state", que guarda o status
    #       de cada serviço do Counter-Strike 2.
    #
        
    api = requests.get('https://ares.lunxi.dev/status')
    response = api.json()["data"]["status"]
    os.system('cls')
    print(f"[Ares API] {api_status_dictionary[api.status_code]}")


    last_state.update(state)
    state.clear()

    sessions_logon = response['services']['SessionsLogon']
    community = response['services']['SteamCommunity']
    matchmaker = response['matchmaker']['scheduler']

    state.update({ 
        "sessions_logon": sessions_logon, 
        "community": community, 
        "matchmaker": matchmaker, 
        })

def embed_function():
    embed = discord.Embed()
    embed.title = "Counter-Strike 2 — Serviços"
    embed.description =f"""
    Sessões: `{status_dictionary[state['sessions_logon']]}`
    Comunidade: `{status_dictionary[state['community']]}`
    Criador de partidas: `{status_dictionary[state['matchmaker']]}`
    \nPara invocar essa mensagem, digite `cs caiu` ou `>status`."""

    embed.color = discord.Color.blue()
    return embed

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
    
    embed = embed_function()

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
        embed = embed_function()
        await message.reply(embed=embed)
#
#   Threading...
#       Utilizando uma função de Threading, podemos rodar funções cíclicas ou loops
#       que não bloqueiam o código principal de funcionar, permitido o funcionamento
#       de todo código sem esperar.

async def thread():
    starttime = time.time()
    while True:
        await embed_services()
        await get_services()
        time.sleep(5 - ((time.time() - starttime) % 5))

#
#   Inicialização
#       Após o BOT inicializar, logo chamamos o asyncio para criar uma tarefa assíncrona
#       Essa tarefa assíncrona segura a função de obtenção de dados da API, a cada 30 
#       segundos essa tarefa é cumprida.

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    threading.Thread(target=lambda: asyncio.run(thread())).start()


