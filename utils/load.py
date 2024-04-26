import requests
import json
import os
from utils.dictionaries import api_status_dictionary

async def load():
    with open('state.json', 'r+') as f:
        open_state = json.load(f)
        f.seek(0)
        state = open_state["state"]
        
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

        state["sessions_logon"] = response['services']['SessionsLogon']
        state["community"] = response['services']['SteamCommunity']
        state["matchmaker"] = response['matchmaker']['scheduler']


        json.dump(open_state, f, indent=4)
        f.truncate()
    return True