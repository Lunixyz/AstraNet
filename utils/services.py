import discord
from utils.dictionaries import status_dictionary

async def get_services(client: discord.Client, channel_id: int, state: dict, last_state: dict):
    channel = client.get_channel(channel_id)
    embed = discord.Embed()

    print(f"[Sessions] {state['sessions_logon']}")
    print(f"[Community] {state['community']}")
    print(f"[Matchmaker] {state['matchmaker']}")

    if not channel:
        return

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

    state.clear()