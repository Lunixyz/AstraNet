import json
import discord
from utils.dictionaries import status_dictionary

#
#   embed_function()
#       Essa função irá criar uma Embed utilizando a lib do Discord.py,
#       logo depois disso, irá abrir o arquivo "state.json" com a permi-
#       ssão "r" (leitura), e então, definirá o título, descrição e cor
#       da Embed.      
#

def embed_function():
    embed = discord.Embed()
    with open('state.json', 'r') as f:
        open_state = json.load(f)
        state = open_state["state"]

        embed.title = "Counter-Strike 2 — Serviços"
        embed.description =f"""
        Sessões: `{status_dictionary[state['sessions_logon']]}`
        Comunidade: `{status_dictionary[state['community']]}`
        Criador de partidas: `{status_dictionary[state['matchmaker']]}`
        \nPara invocar essa mensagem, digite `cs caiu` ou `>status`."""
        embed.color = discord.Color.blue()

    return embed