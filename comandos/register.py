import discord
from discord.ext import commands
from models import Obter_Usuario


class RegisterModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Registrar Usuário")
    usuario_db = Obter_Usuario.Manipular_Usuario

    nome_usuario = discord.ui.TextInput(label="Nome", placeholder="Digite um nome de usuario", max_length=28)
    descricao_usuario = discord.ui.TextInput(label='Descrição', placeholder="Escreva uma descrição", max_length=255, style=discord.TextStyle.long)
    rede_social = discord.ui.TextInput(label="Social", placeholder="Coloque o link de um rede social sua")
    pronome = discord.ui.TextInput(label="Pronomes" ,placeholder="Escreva seus pronomes (opicional)", max_length=8,required=False)
    async def on_submit(self, interaction: discord.Interaction):

        id_discord = interaction.user.id
        print(id_discord)
        usuario_novo = self.usuario_db.obter_usuario(str(id_discord))
        apelido = self.nome_usuario.value
        descricao = self.descricao_usuario.value
        social_rede = self.rede_social.value
        pronome = self.pronome.value or "N/a"
        message = ""
        if not usuario_novo:
            # Registra ou atualiza o usuário no banco
            usuario = self.usuario_db.criar_usuario(id_discord, apelido, descricao,social_rede, pronome)
            message = "usuario criado!"
            print(message)
        elif usuario_novo:
            usuario = self.usuario_db.atualizar_usuario(id_discord, apelido, descricao,social_rede, pronome)
            message = "usuario atualizado!"
            print(message)

        await interaction.response.send_message(
            f"Registro completado!",
            ephemeral=True
        )

class Registrar(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="registrar", description="Abra o modal de registro")
    async def registrar(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RegisterModal())

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog Registrar carregado com sucesso!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Registrar(bot))
