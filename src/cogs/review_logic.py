from discord.ext import commands
from discord import app_commands
from menus.review import ReviewMenu
import discord
import os
import json


class Reputation(commands.GroupCog, name="análise"):
    def __init__(self, bot: commands.Bot) -> commands.Bot:
        self.bot = bot

    @app_commands.command(name="efetuar", description="Faça uma análise a um usuário")
    @app_commands.describe(nota="Avalie o serviço feito pelo membro")
    async def add(
        self,
        interaction: discord.Interaction,
        usuario: discord.User,
        nota: app_commands.Range[int, 0, 5],
    ):
        if interaction.user.id == usuario.id:
            content = "Você não pode fazer uma análise de si mesmo!"
            return await interaction.response.send_message(
                content=content, ephemeral=True
            )
        await interaction.response.send_modal(
            ReviewMenu(uid=usuario.id, review_value=nota)
        )

    @app_commands.command(
        name="status", description="Verifique o estado da reputação de um usuário"
    )
    async def list(self, interaction: discord.Interaction, usuario: discord.User):

        with open(f"{os.getcwd()}/user_data/users.json", "r", encoding="utf-8") as f:
            j = json.load(f)

            review_raw = []
            review_raw_text = []

            for user in j["users"]:
                if user["id"] == usuario.id:
                    for review in user["reviews"]:
                        review_raw.append(review["review_value"])
                        review_raw_text.append(
                            {
                                "id": review["id"],
                                "text": review["text"],
                                "value": review["review_value"],
                                "date": review["review_date"],
                                "review_id": review["review_id"],
                            }
                        )

            usr = await self.bot.fetch_user(usuario.id)
            avg = None
            try:
                avg = sum(review_raw) / len(review_raw)
            except ZeroDivisionError:
                avg = 0

            embed = discord.Embed(
                title="\u200b",
                color=discord.Color.blurple(),
            )
            embed.add_field(
                name="\u200b",
                value="> *Utilize `/análise efetuar` para adicionar algo aqui.*",
            )
            embed.add_field(
                name=f"Análises de `{usr.display_name}`", value="\u200b", inline=True
            )
            embed.add_field(
                name="\u200b",
                value=f"> *A nota média deste usuário é de {round(avg, 1)}/5.0 estrelas.*",
            )
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(
                name=f"Últimas {len(review_raw_text[0:6])} análise(s)",
                value="",
            )
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            if len(review_raw_text) == 0:
                embed.add_field(
                    name=f"{self.bot.user.global_name} - :heart:",
                    value='*"Não há nenhuma análise aqui :("*\n - Agora',
                    inline=True,
                )
            for rv in review_raw_text[0:6]:
                usr = self.bot.get_user(rv["id"])
                embed.add_field(
                    name=f"{usr.global_name[0:10]} - {rv['value']}/5 ⭐",
                    value=f"\"*{rv['text']}*\"\n- {rv['date']}",
                    inline=True,
                )

            for _ in range(0, 6 - len(review_raw_text)):
                embed.add_field(name="\u200b", value="", inline=True)

            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reputation(bot))
