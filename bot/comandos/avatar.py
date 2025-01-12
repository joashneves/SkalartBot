import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def avatar(self, ctx: commands.Context, membro: discord.Member = None):
        membro = membro or ctx.author  # Usa o autor se nenhum membro for passado
        await ctx.send(membro.avatar)
    
async def setup(bot):
    await bot.add_cog(Avatar(bot))