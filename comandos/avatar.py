import discord
from discord import app_commands
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx: commands.Context, membro: discord.Member = None):
        membro = membro or ctx.author  # Usa o autor se nenhum membro for passado
        await ctx.send(membro.avatar)

    @app_commands.command()
    async def slash_avatar(self, interect:discord.Integration):
        await interect.response.send_message(interect.user.avatar)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
