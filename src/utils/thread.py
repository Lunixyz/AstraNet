import time
from utils.load import loader
from utils.services import cs_services
import asyncio


class thread:
    def __init__(self, bot, channel_id, role_id):
        self.bot = bot
        self.channel_id = channel_id
        self.role_id = role_id

    async def setup(self):
        starttime = time.time()

        while True:
            services = False

            while services is False:
                try:
                    load = loader(self.bot)
                    services = load.main_loader(self.channel_id)
                except services is True:
                    break

            await cs_services(self.bot).check_services(self.channel_id, self.role_id)
            await asyncio.sleep(5 - ((time.time() - starttime) % 5))
