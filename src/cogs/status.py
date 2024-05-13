from discord.ext import commands
from utils.embed import embed
import discord


class Status(commands.Cog):
    def __init__(self, bot: commands.Bot) -> commands.Bot:
        self.bot = bot

    @commands.Command
    async def status(self, ctx: commands.Context):
        await ctx.message.reply(embed=embed().setup())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content.lower().startswith("cs caiu"):
            await message.add_reaction("❓")

    @commands.Cog.listener()
    async def on_reaction_add(self, ctx: discord.Reaction, user: discord.User):
        if user != ctx.message.author:
            return

        if ctx.emoji != "❓":
            return

        await ctx.message.reply(embed=embed().setup())
        await ctx.remove(self.bot.user)


async def setup(bot: commands.Bot):
    await bot.add_cog(Status(bot))
