import os
import subprocess
import threading
import json
import discord
from discord.ext import commands

class changenumber_check(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def read_output(self, process, process_name):
        for line in iter(process.stdout.readline, b''):
            if line:
                print(f"-> [{process_name} I/O] {line.strip()}")
        for line in iter(process.stderr.readline, b''):
            if line:
                print(f"-> [{process_name} Error] {line.strip()}")

    async def setup(self):
        data_engine = subprocess.Popen(
            [f"{os.getcwd()}/data_engine/data_engine.exe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1)
        data_engine.stdin.write("730\n")
        data_engine.stdin.flush()
        threading.Thread(target=self.read_output, args=(data_engine, "Radon")).start()
        await self.check_changenumber();


    async def check_changenumber(self):
       

        with open(f"{os.getcwd()}/data_engine/data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

            if data["730"]["changenumber_diff"]["has_difference"]:
                file = open(f"{os.getcwd()}/config.json")
                config = json.load(file)
                channel = self.bot.get_channel(int(config["channel"]))

                embed = discord.Embed(
                title="Counter-Strike 2 — Change Number", 
                description="Astra detected that the change number was altered.",
                color=discord.Color.green())

                embed.add_field(
                name="Latest change number:", 
                value=f"`{str(data['730']['changenumber_diff']['latest_changenumber'])}`", inline=True
                )
                
                embed.add_field(
                name="Old change number:",
                value=f"`{str(data['730']['changenumber_diff']['old_changenumber'])}`", inline=True
                )
                
                await channel.send(embed=embed)

