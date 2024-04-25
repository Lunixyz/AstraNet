import time
import os
from utils.embeds import load
from utils.services import get_services
import asyncio
import discord

async def thread(client: discord.Client, channel_id: int, state: dict, last_state: dict):
    starttime = time.time()
    while True:
        os.system("cls")
        print("[Internal] Running thread loop")
        services = False

        while services is False:
            try:
                services = await load(state, last_state)
            except services is True:
                break

        await get_services(client, channel_id, state, last_state)
        
        await asyncio.sleep(30 - ((time.time() - starttime) % 30))