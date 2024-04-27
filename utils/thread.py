import time
import os
from utils.load import load
from utils.services import get_services
import asyncio
import discord

#
#   thread(client, channel_id, role_id)
#       Essa função é responsável para rodar loop principal
#       do código inteiro, ela irá juntar todas as outras em
#       um local só.    
#

async def thread(client: discord.Client, channel_id: int, role_id: int):
    starttime = time.time()

    while True:
        os.system("cls")
        print("[Internal] Running thread loop")
        services = False

        while services is False:
            try:
                services = await load()
            except services is True:
                break

        await get_services(client, channel_id, role_id)
        
        await asyncio.sleep(30 - ((time.time() - starttime) % 30))