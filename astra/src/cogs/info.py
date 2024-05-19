from discord.ext import commands
from discord import app_commands
import discord
import requests
from utils.dictionaries import api_status_dictionary
import json


class Register(commands.GroupCog, name="steam"):
    def __init__(self, bot) -> commands.Bot:
        self.bot = bot
        self.embed = discord.Embed()

    @app_commands.command(
        name="app", description="Get information about a Steam application."
    )
    async def app(self, interaction: discord.Interaction, appid: str):
        response = None

        try:
            api = requests.get(f"http://localhost:3000/app/{appid}/info")
            response = api.json()["data"]["apps"][appid]
        except (json.JSONDecodeError, requests.exceptions.Timeout):
            print("Received an invalid response from the Ares API.")
            await interaction.response.send_message("Erro interno da API.")
            return None

        if response["missingToken"]:
            return await interaction.response.send_message(
                "This application can't be accessed."
            )

        self.embed.set_author(f"${response['appinfo']['common']['name'] or '???'}")

        self.embed.add_field(
            name="Change Number", value=f"#{response['changenumber']}", inline=True
        )
        self.embed.add_field(
            name="Steam Asset Time",
            value=f"#{response['appinfo']['common']['store_asset_mtime'] * 1000}",
            inline=True,
        )
        self.embed.add_field(
            name="Primary Cache",
            value=f"#{response['appinfo']['extended']['primarycache'] or 'Unknown'}",
            inline=True,
        )
        self.embed.add_field(
            name="OS",
            value=f"#{response['appinfo']['common']['oslist'].split(',').join(', ') or 'Unknown'}",
            inline=True,
        )
        self.embed.set_thumbnail(
            f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/${appid}/${response['appinfo']['common']['icon']}.jpg"
        )

        interaction.response.send_message(embed=self.embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Register(bot))
