import discord
from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Latência em milissegundos
        await ctx.send(f"Pong! Latência: {latency}ms")

    @app_commands.command(name="ping", description="Verifique a latência do bot")
    async def ping_slash(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # Latência em milissegundos
        await interaction.response.send_message(f"Pong! Latência: {latency}ms")


async def setup(bot):
    await bot.add_cog(Ping(bot))
