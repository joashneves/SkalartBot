"""
Módulo principal para inicializar o bot Discord.
"""
import random
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from pathlib import Path
from models import Obter_cargo
from models.db import _Sessao, Usuario

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # pylint: disable=no-member

# Permissões e afins
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

"""Atribui um único cargo automaticamente a novos membros, caso o membro não tenha nenhum dos cargos."""


async def atribuir_cargos(member: discord.Member):
    id_guild = str(member.guild.id)
    cargos_ids = Obter_cargo.Manipular_Cargo.obter_Cargo(id_guild)
    print(f"Verificando cargos para o guild_id: {id_guild}")
    # Verifica se o membro já possui algum dos cargos
    cargos_do_membro = [
        cargo for cargo in member.roles if cargo.id in map(int, cargos_ids)
    ]
    if cargos_do_membro:
        print(f"{member.name} já tem um dos cargos, ignorando atribuição.")
        return  # Ignora se o membro já tem um dos cargos
    # Escolher um cargo aleatório da lista de cargos
    if cargos_ids:
        cargo_id = random.choice(cargos_ids)  # Escolher um cargo aleatoriamente
        cargo = discord.utils.get(member.guild.roles, id=int(cargo_id))
        if cargo and cargo not in member.roles:
            await member.add_roles(cargo)
            print(f"Cargo {cargo.name} atribuído a {member.name}.")


# Criação do bot de forma síncrona
bot = commands.Bot(command_prefix="$", intents=permissoes)


async def carregar_comandos():
    for arquivo in os.listdir("comandos"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")


# Evento quando um membro entra no servidor
@bot.event
async def on_member_join(member: discord.Member):
    """Atribui cargos automaticamente quando um membro entra no servidor."""
    await atribuir_cargos(member)


@bot.event
async def on_ready():
    print("Inciand...")
    """Atribui cargos automaticamente a todos os membros ao iniciar o bot."""
    for guild in bot.guilds:
        print(f"Processando guild: {guild.name} (ID: {guild.id})")
        for member in guild.members:
            if not member.bot:  # Ignorar bots
                print(f"Atribuindo cargos para {member.name}")
                await atribuir_cargos(member)
    await carregar_comandos()
    try:
        synced = await bot.tree.sync()  # Sincroniza os comandos de barra
        print(f"Comandos de barra sincronizados: {len(synced)} comandos")
    except Exception as e:
        print(f"Erro ao sincronizar comandos de barra: {e}")
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
