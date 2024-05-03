import requests
import json
import os
import discord
from discord.ext import commands
from utils.dictionaries import api_status_dictionary

#
#   Load()
#       Essa função irá abrir o arquivo "state.json" (com o método open)
#       utilizando as permissões "r+" (escrita + leitura) e então irá
#       ler o JSON dentro deste arquivo. Após ler, ele definirá todos os
#       valores dentro do objeto "state" para suas respectivas respostas
#       da API.
#


async def load(client: commands.Bot, channel_id: str):

    with open(f"{os.getcwd()}/../state.json", "r+") as f:
        open_state = json.load(f)
        state = open_state["state"]

        api = requests.get("https://ares.lunxi.dev/status")
        try:
            response = api.json()["data"]["status"]
        except json.JSONDecodeError:
            os.system("cls")
            print("Received an invalid response from the Ares API.")
            return False
        except requests.exceptions.Timeout:
            os.system("cls")
            print("Ares API timed out.")
            return False

        if response["services"] == "unknown" and response["matchmaking"] == "unknown":
            channel = client.get_channel(channel_id)
            embed = discord.Embed()

            if not channel:
                return 

            content = " O seguinte serviço está fora do ar:"

            embed.title = "API"
            embed.description = "A API da Steam se encontra fora do ar. Rede Counter-Strike inacessível."

            embed.color = discord.Color.red()
            await channel.send(content=content, embed=embed)
            return False

        os.system("cls")
        print(f"[Astra API] {api_status_dictionary[api.status_code]}")
        if api.status_code != 200:
            return False

        state["sessions_logon"] = response["services"]["SessionsLogon"]
        state["community"] = response["services"]["SteamCommunity"]
        state["matchmaker"] = response["matchmaker"]["scheduler"]

        open_state["state"] = state

        f.seek(0)
        json.dump(open_state, f, indent=4)
        f.truncate()

    return True
