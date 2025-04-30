import discord
from discord.ext import commands
from discord import app_commands
import random
from models import Obter_cargo


class ConfirmarRoletaView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, bot: discord.Client):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.bot = bot

    @discord.ui.button(label="Sim", style=discord.ButtonStyle.success)
    async def confirmar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message("Você não tem permissão para usar este botão.", ephemeral=True)
            return
            # Apagar a mensagem original com os botões antes de começar a tarefa

        # Apagar a mensagem original que contém o botão
        await interaction.message.delete()

        message = await interaction.channel.send("Roletando os cargos...")
        guild = self.interaction.guild
        id_guild = str(guild.id)
        print(f"Esta pensando em : Guild ID: {id_guild}")

        cargos_ids = Obter_cargo.Manipular_Cargo.obter_Cargo(id_guild)
        cargos_validos = [discord.utils.get(guild.roles, id=int(cid)) for cid in cargos_ids]
        cargos_validos = [c for c in cargos_validos if c]

        if not cargos_validos:
            await message.edit(content="❌ Os cargos não existem mais no servidor.", view=None)
            return

        membros_afetados = 0
        bot_member = guild.get_member(self.bot.user.id)
        bot_top_role = bot_member.top_role

        for member in guild.members:
            if member.bot:
                continue

            cargos_do_membro_para_remover = [
                cargo for cargo in member.roles
                if cargo < bot_top_role and cargo in cargos_validos
            ]

            if cargos_do_membro_para_remover:
                print(f"Ação: Removendo cargos de {member.name}: {[c.name for c in cargos_do_membro_para_remover]}")
                await member.remove_roles(*cargos_do_membro_para_remover)

            if not any(cargo in member.roles for cargo in cargos_validos):
                novo_cargo = random.choice(cargos_validos)
                await member.add_roles(novo_cargo)
                membros_afetados += 1
                print(f"Ação: {member.name} recebeu o cargo {novo_cargo.name}")

        print(f"Rerolagem concluída. Total de membros afetados: {membros_afetados}")
    
        # Edita a mensagem original com os botões desativados
        await message.edit(
            content=f"✅ Todos os cargos foram rerolados!\n👥 Membros afetados: `{membros_afetados}`.",
            view=None
        )


    @discord.ui.button(label="Não", style=discord.ButtonStyle.danger)
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message("Você não pode cancelar esta ação.", ephemeral=True)
            return
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        await interaction.response.edit_message(content="❌ Ação cancelada.", view=self)

class Cargos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="configurar_cargo",
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

    @app_commands.command(name="roletar_cargo", description="Rerola todos os cargos do servidor.")
    @app_commands.default_permissions(manage_guild=True)
    async def roletar_cargo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="⚠️ Confirmação Necessária",
            description="Essa ação é **IRREVERSÍVEL**!\nDeseja realmente rerolar os cargos de todos os membros?",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, view=ConfirmarRoletaView(interaction, self.bot))

    @app_commands.command(
        name="remover_cargo",
        description="Remove um cargo da lista de cargos salvos.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def remover_cargo(
        self, interaction: discord.Interaction, cargo: discord.Role
    ):
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
