import discord
from discord.ext import commands
from discord import app_commands
from models.Obter_Feed import Manipular_Feed


class Feed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="configurar_feed", description="Configura um canal para receber feeds."
    )
    @app_commands.describe(channel="O canal onde os feeds serão enviados.")
    @app_commands.default_permissions(manage_guild=True)
    async def configurar_feed(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_id = str(interaction.guild_id)
        channel_id = str(channel.id)

        # Adiciona o canal de feed ao banco de dados
        feed = Manipular_Feed.adicionar_chat(guild_id, channel_id)
        if feed:
            await interaction.response.send_message(
                f"Canal {channel.mention} configurado para receber feeds.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Erro ao configurar o canal de feed.", ephemeral=True
            )

    @app_commands.command(
        name="remover_feed",
        description="Remove um canal da lista de feeds configurados.",
    )
    @app_commands.describe(
        channel="O canal que será removido da configuração de feeds."
    )
    @app_commands.default_permissions(manage_guild=True)
    async def remover_feed(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_id = str(interaction.guild_id)
        channel_id = str(channel.id)

        # Remove o canal de feed do banco de dados
        removido = Manipular_Feed.remover_chat(channel_id)
        if removido:
            await interaction.response.send_message(
                f"Canal {channel.mention} removido da configuração de feeds.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Canal {channel.mention} não estava configurado para feeds.",
                ephemeral=True,
            )

    @app_commands.command(
        name="listar_feeds",
        description="Lista todos os canais configurados para receber feeds.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def listar_feeds(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)

        # Lista todos os canais de feed configurados
        feeds = Manipular_Feed.listar_chats(guild_id)
        if not feeds:
            await interaction.response.send_message(
                "Nenhum canal configurado para receber feeds.", ephemeral=True
            )
            return

        # Formata a lista de canais de feed
        lista_feeds = "\n".join([f"<#{feed.channel_id}>" for feed in feeds])
        await interaction.response.send_message(
            f"Canais de feed configurados:\n{lista_feeds}", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Feed(bot))
