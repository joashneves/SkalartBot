import os
import discord
from discord.ext import commands
from discord import app_commands
from models import Obter_Usuario
from models.Obter_imagem import Manipular_Imagem
from dotenv import load_dotenv
import random

load_dotenv()  # Carregar as variáveis do .env
ID_USER_MASTER = int(os.getenv("ID_USER_MASTER"))  # Pegar o ID do User Master


class AdicionarImagem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="adicionar_imagem",
        description="Adiciona uma imagem ao banco de dados. Só pode enviar uma por dia!"
    )
    async def adicionar_imagem(self, interaction: discord.Interaction, imagem: discord.Attachment, descricao: str):
        id_discord = str(interaction.user.id)

        # Verifica se o usuário está registrado
        usuario_registrado = Obter_Usuario.Manipular_Usuario.obter_usuario(id_discord)
        if not usuario_registrado:
            await interaction.response.send_message(
                "Você precisa estar registrado para enviar uma imagem! Use `/registrar`.",
                ephemeral=True
            )
            return
        # Salva o caminho da imagem (URL do Discord)
        caminho_arquivo = imagem.url

        # Gera moedas e xp aleatórios
        moedas_ganhas = random.randint(10, 50)  # Gera entre 10 e 50 moedas
        xp_ganho = random.randint(1, 5)  # Gera entre 1 e 3 xp

        # Salva o caminho da imagem (URL do Discord)
        caminho_arquivo = imagem.url
        # Adiciona a imagem ao banco
        print(id_discord, caminho_arquivo, descricao)
        sucesso = Manipular_Imagem.criar_Imagem(id_discord, caminho_arquivo, descricao)
        print(sucesso)
        if sucesso:
            await interaction.response.send_message(
                f"Imagem adicionada com sucesso!\n **Descrição:** {descricao}\n [Clique para ver a imagem]({caminho_arquivo})"
            )
            usuario_atualizado = Obter_Usuario.Manipular_Usuario.adicionar_moedas(id_discord, moedas_ganhas)
            usuario_atualizado = Obter_Usuario.Manipular_Usuario.adicionar_xp(id_discord, xp_ganho)
            if not usuario_atualizado:
                await interaction.response.send_message(
                    "Erro ao adicionar moedas ou moedas. Tente novamente.",
                    ephemeral=True
                )
                return
            print(f"Saldo e xp adicionado em : {usuario_atualizado}")
        else:
            await interaction.response.send_message(
                "Ocorreu um erro ao salvar a imagem. Tente novamente.",
                ephemeral=True
            )

    @app_commands.command(
        name="imagem_aleatoria",
        description="Mostra uma imagem aleatória enviada por qualquer pessoa!"
    )
    async def imagem_aleatoria(self, interaction: discord.Interaction):
        imagem = Manipular_Imagem.obter_imagem_aleatoria()

        if imagem:
            usuario = await self.bot.fetch_user(int(imagem.id_discord))  # Obtém o usuário do Discord

            embed = discord.Embed(
                title="🖼️ Imagem Aleatória",
                description=f"**Descrição:** {imagem.descricao}",
                color=discord.Color.blue()
            )
            embed.set_image(url=imagem.caminho_arquivo)

            embed.set_footer(text=f"Enviado por: {usuario.name}", icon_url=usuario.display_avatar.url)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "Nenhuma imagem encontrada no banco de dados!",
                ephemeral=True
            )

    @app_commands.command(
        name="remover_imagem",
        description="Remove uma imagem que você enviou."
    )
    @app_commands.describe(imagem_id="O ID da imagem que você deseja remover.")
    async def remover_imagem(self, interaction: discord.Interaction, imagem_id: int):
        id_discord = str(interaction.user.id)

        # Remove a imagem
        sucesso = Manipular_Imagem.remover_imagem(id_discord, imagem_id)
        if sucesso:
            await interaction.response.send_message(
                f"✅ Imagem com ID **{imagem_id}** foi removida com sucesso!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"⚠️ Não foi possível encontrar uma imagem com o ID **{imagem_id}** enviada por você.", ephemeral=True
            )

    @app_commands.command(
        name="minhas_imagens",
        description="Lista todas as imagens que você enviou."
    )
    async def minhas_imagens(self, interaction: discord.Interaction):
        id_discord = str(interaction.user.id)

        # Lista as imagens do usuário
        imagens = Manipular_Imagem.listar_imagens_usuario(id_discord)
        if not imagens:
            await interaction.response.send_message(
                "⚠️ Você ainda não enviou nenhuma imagem.", ephemeral=True
            )
            return

        # Formata a lista de imagens
        lista_imagens = "\n".join(
            [f"**ID:** {imagem.id} | **Descrição:** {imagem.descricao} | [Ver imagem]({imagem.caminho_arquivo})"
             for imagem in imagens]
        )

        embed = discord.Embed(
            title="📸 Suas Imagens",
            description=lista_imagens,
            color=discord.Color.blue()
        )
        embed.set_footer(text="Use /remover_imagem <ID> para remover uma imagem.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="remover_imagens",
        description="Remove todas as imagens enviadas por um usuário específico. (Apenas User Master)"
    )
    @app_commands.default_permissions(administrator=True)
    async def remover_imagens(self, interaction: discord.Interaction, usuario: discord.User):
        # Verifica se o usuário que usou o comando é o Master
        if interaction.user.id != ID_USER_MASTER:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando!", ephemeral=True
            )
            return

        # Remove todas as imagens do usuário fornecido
        sucesso = Manipular_Imagem.remover_todas_imagens(str(usuario.id))

        if sucesso:
            await interaction.response.send_message(
                f"✅ Todas as imagens enviadas por **{usuario.name}** foram removidas!"
            )
        else:
            await interaction.response.send_message(
                f"⚠️ Nenhuma imagem encontrada para **{usuario.name}**.", ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(AdicionarImagem(bot))
