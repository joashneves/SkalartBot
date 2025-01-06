import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
# Permissões e afins
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix='&', intents=permissoes)

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} está online!")


bot.run(TOKEN)
