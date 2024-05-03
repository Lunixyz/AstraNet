from discord.ext import commands
from discord import app_commands
import discord
import os
import json


class Admin(commands.GroupCog, name="admin"):
    def __init__(self, bot) -> commands.Bot:
        self.bot = bot

    @app_commands.command(
        name="análise_remover", description="Remova uma análise específica"
    )
    async def remove(
        self, interaction: discord.Interaction, usuario: discord.User, analise_id: str
    ):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                content="Você não é administrador, não é possível executar esse comando."
            )

        with open(f"{os.getcwd()}/user_data/users.json", "r+", encoding="utf-8") as f:
            j = json.load(f)

            for user in j["users"]:
                for reviews in user["reviews"]:
                    if reviews["review_id"] == analise_id:
                        user["reviews"].pop(user["reviews"].index(reviews))

            f.seek(0)
            f.truncate()
            json.dump(j, f, indent=4, ensure_ascii=False)
            f.close()

        await interaction.response.send_message(
            content=f"Análise com o ID `{analise_id}` removida.", ephemeral=True
        )

    @app_commands.command(
        name="análise_lista",
        description="veja a lista completa de análises de um usuário",
    )
    async def list(self, interaction: discord.Interaction, usuario: discord.User):
        with open(f"{os.getcwd()}/user_data/users.json", "r+", encoding="utf-8") as f:
            j = json.load(f)

            string = "```ml\n\n"

            for user in j["users"]:
                if user["id"] == usuario.id:
                    for review in user["reviews"]:
                        usr = await self.bot.get_user(review["id"])
                        string += (
                            f'Nome: "{usr.global_name}"'
                            f"\n├ Texto: \"{review['text']}\""
                            f"\n├ Estrelas: {review['review_value']}/5"
                            f"\n└ Review-ID: {review['review_id']}\n"
                            "\n"
                        )
            string += "```"

        await interaction.response.send_message(content=string, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
