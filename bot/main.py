"""
Módulo principal para inicializar o bot Discord.
"""

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from pathlib import Path

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # pylint: disable=no-member

# Permissões e afins
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

# Criação do bot de forma síncrona
bot = commands.Bot(command_prefix="$", intents=permissoes)

# Função para carregar os comandos
async def carregar_comandos():
    """
    Carrega os comandos do bot dinamicamente a partir do diretório bot/comandos.
    """
    comandos_path = Path("bot") / "comandos"  # Constrói o caminho portátil
    for arquivo in comandos_path.glob("*.py"):  # Encontra todos os arquivos .py
        await bot.load_extension(
            f"bot.comandos.{arquivo.stem}"
        )  # Usa o nome sem extensão


@bot.event
async def on_ready():
    """
    Evento disparado quando o bot é inicializado com sucesso.
    """
    await carregar_comandos()
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
