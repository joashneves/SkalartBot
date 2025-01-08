import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from pathlib import Path

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
# Permissões e afins
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix='$', intents=permissoes)

async def carregar_comandos():
    comandos_path = Path("bot") / "comandos"  # Constrói o caminho portátil
    for arquivo in comandos_path.glob('*.py'):  # Encontra todos os arquivos .py
        await bot.load_extension(f"bot.comandos.{arquivo.stem}")  # Usa o nome sem extensão

@bot.event
async def on_ready():
    await carregar_comandos()
    print(f"Bot {bot.user.name} está online!")

bot.run(TOKEN)
