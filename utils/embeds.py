import json
import discord
from utils.dictionaries import status_dictionary


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