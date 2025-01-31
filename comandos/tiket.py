import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput


class TiketModel(Modal):
    def __init__(self):
        super().__init__(title="Abrir ticket")

    titulo = TextInput(label="Resuma seu ticket")
    descricao = TextInput(
        label="Descreva o ticket",
        style=discord.TextStyle.long,
    )

    async def on_submit(self, interact: discord.Interaction):
        categoria_tiket = discord.utils.get(
            interact.guild.categories, id=1334965351053529251
        )
        ticket_canal = await interact.guild.create_text_channel(
            f"TICKET-{interact.user.name}", category=categoria_tiket
        )
        await ticket_canal.set_permissions(interact.user, view_channel=True)
        ticket_canal = await ticket_canal.send(
            f"# Tiker de {interact.user.name} \n ## {self.titulo} \n > {self.descricao}"
        )
        await interact.response.send_message(
            f"# Tiket criado em {ticket_canal} \n", ephemeral=True
        )


class Tiket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="enviar_ticket", description="Envia um ticket")
    async def enviar_ticker(self, interact: discord.Interaction):
        await interact.response.send_modal(TiketModel())

    @app_commands.command(
        name="fechar_ticket", description="Fecha o ticket que voce esta"
    )
    async def fechar_ticker(self, interact: discord.Interaction):
        categoria_tiket = discord.utils.get(
            interact.guild.categories, id=1334965351053529251
        )
        if categoria_tiket != interact.channel.category:
            await interact.response.send_message(
                f"Voce só pode usar esse comando em um ticket", ephemaral=True
            )
            return
        everyone = interact.guid.default_role
        await interact.channel.set_permissions(everyone, send_messages=False)
        await interact.response.send_modal(TiketModel())


async def setup(bot: commands.Bot):
    await bot.add_cog(Tiket(bot))
