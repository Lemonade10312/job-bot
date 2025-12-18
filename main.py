import os
import discord
from discord import app_commands
from discord.ui import Button, View


ADMIN_CHANNEL_ID = 1451254315556802641  


class ApplyButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            Button(
                label="応募する",
                style=discord.ButtonStyle.success,
                custom_id="apply_button"
            )
        )


class JobBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = JobBot()


@client.tree.command(name="job", description="求人募集を投稿します")
@app_commands.describe(
    title="求人タイトル",
    price="料金",
    content="依頼内容"
)
async def job(interaction: discord.Interaction, title: str, price: str, content: str):
    embed = discord.Embed(title="📢 求人募集", color=0x2ecc71)
    embed.add_field(name="■ タイトル", value=title, inline=False)
    embed.add_field(name="■ 料金", value=price, inline=False)
    embed.add_field(name="■ 依頼内容", value=content, inline=False)
    embed.set_footer(text="下のボタンから応募できます")

    await interaction.response.send_message(embed=embed, view=ApplyButton())


@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data.get("custom_id") == "apply_button":
            await interaction.user.send(
                "📩 **応募ありがとうございます！**\n\n"
                "以下の内容をこのDMに送ってください👇\n"
                "・自己紹介\n"
                "・実績（URL可）\n"
                "・対応可能本数 / 納期"
            )
            await interaction.response.send_message(
                "DMに応募フォームを送りました！",
                ephemeral=True
            )


@client.event
async def on_message(message: discord.Message):
    
    if message.author.bot:
        return

   
    if isinstance(message.channel, discord.DMChannel):
        admin_channel = client.get_channel(ADMIN_CHANNEL_ID)

        if admin_channel:
            embed = discord.Embed(
                title="📨 新しい応募",
                color=0x3498db
            )
            embed.add_field(
                name="応募者",
                value=f"{message.author}（ID: {message.author.id}）",
                inline=False
            )
            embed.add_field(
                name="応募内容",
                value=message.content,
                inline=False
            )

            await admin_channel.send(embed=embed)

            await message.channel.send(
                "✅ 応募内容を送信しました。ご連絡をお待ちください！"
            )

client.run(os.getenv("BOT_TOKEN"))

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

