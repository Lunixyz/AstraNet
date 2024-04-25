import requests
import json
import os
import discord
from utils.dictionaries import api_status_dictionary, status_dictionary

async def load(state: dict, last_state: dict): 
        
    api = requests.get('https://ares.lunxi.dev/status')
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
    return True

def embed_function(state: dict):
    embed = discord.Embed()
    embed.title = "Counter-Strike 2 — Serviços"
    embed.description =f"""
    Sessões: `{status_dictionary[state['sessions_logon']]}`
    Comunidade: `{status_dictionary[state['community']]}`
    Criador de partidas: `{status_dictionary[state['matchmaker']]}`
    \nPara invocar essa mensagem, digite `cs caiu` ou `>status`."""

    embed.color = discord.Color.blue()
    return embed