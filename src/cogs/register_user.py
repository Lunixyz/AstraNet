from discord.ext import commands
import discord
import os
import json


class Register(commands.Cog):
    def __init__(self, bot) -> commands.Bot:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx: discord.Message):

        with open(f"{os.getcwd()}/user_data/users.json", "r+", encoding="utf-8") as f:
            j = json.load(f)
            users = j["users"]

            for user in users:
                if ctx.author.id == user["id"]:
                    return

            template: dict = {"id": ctx.author.id, "reviews": []}

            users.append(template)
            f.seek(0)
            json.dump(j, f, indent=4, ensure_ascii=False)
            f.truncate()
            f.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(Register(bot))
