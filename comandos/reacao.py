import discord
from discord.ext import commands
from discord import app_commands
from models import Obter_Chat
import re


def is_image_url(text: str) -> bool:
    # Expressão regular para verificar URLs de imagens
    image_url_pattern = re.compile(
        r"https?://[^\s]+\.(?:png|jpg|jpeg|gif|webp)", re.IGNORECASE
    )
    return bool(image_url_pattern.search(text))


Manipular_Chat = Obter_Chat.Manipular_Chat


class Reacao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="configurar_chat",
        description="Configura um chat para reagir com emoji em imagens.",
    )
    @app_commands.describe(channel="O canal onde as reações serão ativadas.")
    @app_commands.default_permissions(manage_guild=True)
    async def configurar_chat(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_id = str(interaction.guild_id)
        channel_id = str(channel.id)

        chat = Manipular_Chat.adicionar_chat(guild_id, channel_id)
        if chat:
            await interaction.response.send_message(
                f"Chat {channel.mention} configurado para reagir com emoji em imagens.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Erro ao configurar o chat.", ephemeral=True
            )

    @app_commands.command(
        name="remover_chat",
        description="Remove um chat da lista de canais configurados.",
    )
    @app_commands.describe(channel="O canal que será removido da configuração.")
    @app_commands.default_permissions(manage_guild=True)
    async def remover_chat(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild_id = str(interaction.guild_id)
        channel_id = str(channel.id)

        removido = Manipular_Chat.remover_chat(channel_id)
        if removido:
            await interaction.response.send_message(
                f"Chat {channel.mention} removido da configuração.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Chat {channel.mention} não estava configurado.", ephemeral=True
            )

    @app_commands.command(
        name="listar_chats",
        description="Lista todos os chats configurados no servidor.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def listar_chats(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        chats = Manipular_Chat.listar_chats(guild_id)

        if not chats:
            await interaction.response.send_message(
                "Nenhum chat configurado neste servidor.", ephemeral=True
            )
            return

        # Formata a lista de chats
        lista_chats = "\n".join([f"<#{chat.channel_id}>" for chat in chats])
        await interaction.response.send_message(
            f"Chats configurados:\n{lista_chats}", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        REACTION_EMOJIS = ["👍", "👎", "❤️", "😂", "😠"]
        chat = Manipular_Chat.obter_chat(str(message.channel.id))
        if chat:
            # Verifica se a mensagem contém anexos de imagem
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.lower().endswith(
                        (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4")
                    ):
                        for emoji in REACTION_EMOJIS:
                            await message.add_reaction(emoji)
                        break

            # Verifica se a mensagem contém URLs de imagem
            if is_image_url(message.content):
                for emoji in REACTION_EMOJIS:
                    await message.add_reaction(emoji)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reacao(bot))
