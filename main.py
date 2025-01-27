"""
Módulo principal para inicializar o bot Discord.
"""

import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from pathlib import Path
from models.db import _Sessao, Usuario

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # pylint: disable=no-member

# Permissões e afins
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

# Criação do bot de forma síncrona
bot = commands.Bot(command_prefix="$", intents=permissoes)


async def carregar_comandos():
    for arquivo in os.listdir('comandos'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")

@bot.event
async def on_ready():
    """
    Evento disparado quando o bot é inicializado com sucesso.
    """
    print("print")
    await carregar_comandos()
    await bot.tree.sync()
    print(f"Bot {bot.user.name} está online!")
    return "Bot Online"


# Função main para ser chamada no script
def main():
    """
    Executa o bot utilizando o token armazenado no ambiente.
    """
    bot.run(TOKEN)


# Este bloco só é executado quando o script for rodado diretamente
if __name__ == "__main__":
    main()
