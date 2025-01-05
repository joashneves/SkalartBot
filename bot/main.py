import os
from dotenv import load_dotenv
from discord.ext import commands

# Carrega variáveis do .env
load_dotenv()

# Obtém o token do .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Inicializa o bot
bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Executa o bot com o token
if TOKEN:
    bot.run(TOKEN)
else:
    print("O token do bot não foi encontrado. Verifique o arquivo .env.")
