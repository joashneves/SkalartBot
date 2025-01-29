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
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Você não tem permissão para usar este comando.", ephemeral=True
            )
            return

        id_guild = str(interaction.guild_id)
        id_cargo = str(cargo.id)

        try:
            Obter_cargo.Manipular_Cargo.criar_Cargo(id_guild, id_cargo)
            await interaction.response.send_message(
                f"O cargo {cargo.name} foi adicionado com sucesso!"
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Ocorreu um erro ao adicionar o cargo: {e}", ephemeral=True
            )

    @app_commands.command(
        name="listar_cargos",
        description="Lista todos os cargos salvos no banco de dados.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def listar_cargos(self, interaction: discord.Interaction):
        id_guild = str(interaction.guild_id)
        cargos_ids = Obter_cargo.Manipular_Cargo.obter_Cargo(id_guild)

        if not cargos_ids:
            await interaction.response.send_message(
                "Nenhum cargo salvo foi encontrado.", ephemeral=True
            )
            return

        cargos = []
        for cargo_id in cargos_ids:
            cargo = interaction.guild.get_role(int(cargo_id))
            if cargo:
                cargos.append(cargo.name)

        descricao = "\n".join(cargos) if cargos else "Nenhum cargo encontrado."
        embed = discord.Embed(
            title="Cargos Salvos",
            description=descricao,
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="remover_cargo",
        description="Remove um cargo da lista de cargos salvos.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def remover_cargo(self, interaction: discord.Interaction, cargo: discord.Role):
        id_guild = str(interaction.guild_id)
        id_cargo = str(cargo.id)

        try:
            removido = Obter_cargo.Manipular_Cargo.remover_Cargo(id_guild, id_cargo)
            if removido:
                await interaction.response.send_message(
                    f"O cargo {cargo.name} foi removido com sucesso!"
                )
            else:
                await interaction.response.send_message(
                    "O cargo não estava salvo no banco de dados.", ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"Ocorreu um erro ao remover o cargo: {e}", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Cargos(bot))
