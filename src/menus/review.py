import discord
import json
import os
import random
import hashlib
from datetime import datetime


class ReviewMenu(discord.ui.Modal, title="Análise"):
    def __init__(self, uid: int, review_value: int):
        self.uid = uid
        self.review_value = review_value
        super().__init__()

    text = discord.ui.TextInput(
        custom_id="review_text",
        label="Campo de Texto",
        style=discord.TextStyle.paragraph,
        required=True,
        placeholder="Recebi tudo direitnho...",
        max_length=220,
        min_length=5,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content="Análise feita com sucesso, valeu!", ephemeral=True
        )
        with open(f"{os.getcwd()}/user_data/users.json", "r+", encoding="utf-8") as f:
            j = json.load(f)
            date = datetime.now().strftime("%Y%m%d%H%M%S")
            rand = random.randint(0, 10000)
            concat = date + str(interaction.user.id) + str(rand)
            unique_id = hashlib.sha256(concat.encode()).hexdigest()

            for user in j["users"]:
                if user["id"] == self.uid:
                    user["reviews"].insert(
                        0,
                        {
                            "id": interaction.user.id,
                            "text": self.text.value,
                            "review_value": self.review_value,
                            "review_date": datetime.now().strftime(
                                "%d/%m/%Y, %H:%M:%S"
                            ),
                            "review_id": unique_id,
                        },
                    )
                    break

            f.seek(0)
            f.truncate()
            json.dump(j, f, indent=4, ensure_ascii=False)
            f.close()
