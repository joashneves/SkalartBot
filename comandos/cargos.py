import discord
from discord.ext import commands
from discord import app_commands
from models import Obter_cargo


class Cargos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="adicionar_cargo",
        description="Adiciona um cargo à lista de cargos a serem atribuídos automaticamente.",
    )
    @app_commands.default_permissions(manage_guild=True)
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

        try:
            # Adicionar o cargo ao banco de dados
            Obter_cargo.Manipular_Cargo.criar_Cargo(id_guild, id_cargo)
            await interaction.response.send_message(
                f"O cargo {cargo.name} foi adicionado com sucesso!"
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Ocorreu um erro ao adicionar o cargo: {e}", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Cargos(bot))
    # Registrar o comando de barra no CommandTree
    if not bot.tree.get_command("adicionar_cargo"):
        bot.tree.add_command(Cargos(bot).add_cargo)
