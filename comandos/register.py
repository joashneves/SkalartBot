import discord
from discord.ext import commands
from discord import app_commands
from models import Obter_Usuario
from models.Obter_imagem import Manipular_Imagem


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

class ImageView(discord.ui.View):
    def __init__(self, imagens, usuario):
        super().__init__(timeout=60)  # Timeout de 60 segundos
        self.imagens = imagens
        self.usuario = usuario
        self.index = 0

    async def update_embed(self, interaction: discord.Interaction):
        """Atualiza o embed com a imagem atual."""
        imagem = self.imagens[self.index]
        embed = discord.Embed(
            title=f"📸 Imagens de {self.usuario.name}",
            description=f"Descrição: {imagem.descricao}",
            color=discord.Color.blue()
        )
        embed.set_image(url=imagem.caminho_arquivo)
        embed.set_footer(text=f"De {self.usuario.name} : Imagem {self.index + 1} de {len(self.imagens)}", icon_url=self.usuario.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⬅️ Anterior", style=discord.ButtonStyle.primary)
    async def anterior(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Volta para a imagem anterior."""
        self.index = (self.index - 1) % len(self.imagens)
        await self.update_embed(interaction)

    @discord.ui.button(label="➡️ Próximo", style=discord.ButtonStyle.primary)
    async def proximo(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Avança para a próxima imagem."""
        self.index = (self.index + 1) % len(self.imagens)
        await self.update_embed(interaction)
class Registrar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="registrar", description="Abra o modal de registro")
    async def registrar(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RegisterModal())

    @app_commands.command(
        name="perfil",
        description="Mostra o perfil de um usuário registrado."
    )
    async def perfil(self, interaction: discord.Interaction, usuario: discord.User = None):
        usuario = usuario or interaction.user  # Se não informar um usuário, mostra o próprio perfil
        usuario_db = Obter_Usuario.Manipular_Usuario.obter_usuario(str(usuario.id))

        if not usuario_db:
            await interaction.response.send_message("❌ Este usuário não está registrado!", ephemeral=True)
            return

        # Cria o embed do perfil
        embed = discord.Embed(
            title=f"👤 Perfil de {usuario_db.apelido or 'Usuário'}",
            color=discord.Color.purple()
        )
        embed.add_field(name="📝 Descrição", value=usuario_db.descricao or "Nenhuma descrição.", inline=False)
        embed.add_field(name="🔗 Social", value=usuario_db.rede_social or "Não informado", inline=False)
        embed.add_field(name="🔤 Pronomes", value=usuario_db.pronome or "Não informado", inline=False)
        embed.add_field(name="📊 Level", value=f"{usuario_db.level}", inline=True)
        embed.add_field(name="⭐ XP", value=f"{usuario_db.xp}", inline=True)
        embed.add_field(name="💰 Saldo", value=f"{usuario_db.saldo} moedas", inline=True)
        embed.set_thumbnail(url=usuario.display_avatar.url)  # Mostra o avatar do usuário

        # Verifica se o usuário tem imagens
        imagens = Manipular_Imagem.obter_imagens_por_usuario(str(usuario.id))
        if imagens:
            # Mostra a primeira imagem
            imagem = imagens[0]
            embed.set_image(url=imagem.caminho_arquivo)
            embed.set_footer(text=f"Imagem 1 de {len(imagens)}")

            # Adiciona a view de navegação
            view = ImageView(imagens, usuario)
        else:
            embed.set_footer(text="Este usuário ainda não enviou nenhuma imagem.")
            view = None

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Registrar(bot))
