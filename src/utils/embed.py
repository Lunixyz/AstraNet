import json
import os
import discord
from utils.dictionaries import status_dictionary


class embed(discord.Embed):

    def setup(self):
        with open(f"{os.getcwd()}/../state.json", "r") as f:
            open_state = json.load(f)
            state = open_state["state"]
            self.title = "Counter-Strike 2 — Serviços"
            self.description = f"""
            Sessões: `{status_dictionary[state['sessions_logon']]}`
            Comunidade: `{status_dictionary[state['community']]}`
            Criador de partidas: `{status_dictionary[state['matchmaker']]}`
            \nPara invocar essa mensagem, digite `cs caiu` ou `>status`."""
            self.color = discord.Color.blue()
        return self
