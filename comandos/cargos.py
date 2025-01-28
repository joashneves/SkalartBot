import discord
from discord.ext import commands
from models import Obter_cargo

class Cargos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @discord.app_commands.command(
        name="adicionar_cargo",
        description="Adiciona um cargo à lista de cargos a serem atribuídos automaticamente."
    )
    async def add_cargo(self, interaction: discord.Interaction, cargo: discord.Role):
        # Verificar se o usuário é administrador
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Você não tem permissão para usar este comando.", ephemeral=True
            )
            return

        # Verificar se o cargo existe no servidor
        id_guild = str(interaction.guild_id)
        id_cargo = str(cargo.id)

        # Adicionar o cargo ao banco de dados
        Obter_cargo.Manipular_Cargo.criar_Cargo(id_guild, id_cargo)
        await interaction.response.send_message(f"O cargo {cargo.name} foi adicionado com sucesso!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Cargos(bot))
