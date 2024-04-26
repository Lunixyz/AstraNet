import discord
import json
from utils.dictionaries import status_dictionary, titles

async def get_services(client: discord.Client, channel_id: int, role_id: int):
    with open('state.json', 'r+') as f:
        f.seek(0)

        channel = client.get_channel(channel_id)
        embed = discord.Embed()
        open_state = json.load(f)
        state = open_state["state"]
        last_state = open_state["last_state"]

        if not channel:
            return

        content = f"# Atenção <@{role_id}>!\n ## Status da rede Counter-Strike:"
        
        for service in state:
            print(f"[{titles[service]}] {status_dictionary[state[service]]}")
            
            if state[service] != "normal" and last_state[service] != state[service]:
                last_state[service] = state[service]
                json.dump(open_state, f, indent=4)

                embed.title = titles[service]
                embed.description = f"{titles[service]} está `{status_dictionary[state[service]]}`"
                embed.color = discord.Color.red()
                await channel.send(content=content, embed=embed)

        f.truncate()
