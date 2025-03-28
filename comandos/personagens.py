import discord
from discord import app_commands
from discord.ext import commands
from models.Obter_personagem import Manipular_Personagem
import aiohttp
import hashlib
import os
import json


IMAGENS_DIR = "imagens_temp"
os.makedirs(IMAGENS_DIR, exist_ok=True)

async def carrega_imagem(url) -> str:
    """
    Salva uma imagem localmente e retorna o caminho do arquivo.
    :param url: URL da imagem.
    :param user_id: ID do usuário que enviou a imagem.
    :return: Caminho do arquivo salvo.
    """
    nome_arquivo = f"{hashlib.md5(url.encode()).hexdigest()}.png"
    caminho_arquivo = os.path.join(IMAGENS_DIR, nome_arquivo)

    # Baixa a imagem e salva localmente
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(caminho_arquivo, "wb") as f:
                    f.write(await response.read())
                return caminho_arquivo
            else:
                raise Exception(f"Erro ao baixar imagem: status {response.status}")

class PersonagensView(discord.ui.View):
    def __init__(self, guild_id, membro_id, personages, interaction):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.membro_id = membro_id
        self.personagens = personages
        self.index = 0
        self.caminho = None

    async def update_message(self, interaction):
        caminho_arquivo = await self.imagem()
        print(f"VAR : personagens {self.personagens[self.index]}")

        embed = discord.Embed(
            title=f"Personagem: {self.personagens[self.index].nome_personagem}",
            #description=f"Franquia: c \n Genero: {self.personagens[self.index].genero_personagem} \n Descrição: {self.personagens[self.index].descricao_personagem}",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Franquia",value=f"{self.personagens[self.index].franquia_personagem}",inline=False)
        embed.add_field(name="Genero",value=f"{self.personagens[self.index].genero_personagem}", inline=False)
        embed.add_field(name="Descrição",value=f"{self.personagens[self.index].descricao_personagem}", inline=False)
        embed.set_image(url=f"attachment://image.jpg")
        print(caminho_arquivo)
        embed.set_footer(text=f"Descoberto em : {self.personagens[self.index].data_de_descoberta}")
        await interaction.response.edit_message(embed=embed, view=self, attachments=[caminho_arquivo])
        return embed

    async def imagem(self):
        print(f"VAR: {self.personagens[self.index]}")
        caminho_arquivo = await carrega_imagem(f"https://personagensaleatorios.squareweb.app/api/Personagems/DownloadPersonagemByPath?Path={self.personagens[self.index].caminho_arquivo_personagem}")
        self.caminho = caminho_arquivo
        discord_file = discord.File(caminho_arquivo, 'image.jpg')
        return discord_file

    async def deletar_arquivo(self):
        try:
            if os.path.exists(self.caminho):
                os.remove(self.caminho)
            else:
                return "caminho não encontrado!"
            return f"arquivo deletado do {self.caminho}"
        except:
            return "erro ao apagar arquivo"

    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.primary)
    async def anterior(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = (self.index - 1) % len(self.personagens)
        await self.update_message(interaction)
        res = await self.deletar_arquivo()
        print(f"AÇÃO : {res}")

    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.primary)
    async def proximo(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = (self.index + 1) % len(self.personagens)
        await self.update_message(interaction)
        res = await self.deletar_arquivo()
        print(f"AÇÃO : {res}")

class Personagens(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.command(
        name="listar_personagens",
        description="Lista todos os personagens capturados.",
    )
    async def listar_personagens_slash(self, interaction: discord.Interaction):
        personagens = Manipular_Personagem.obter_todos_personagens_descoberto_usuario(interaction.user.id, interaction.guild.id)
        print(f"Var : Personagens = {personagens}")
        if personagens:
            view = PersonagensView(interaction.guild.id, interaction.user.id, personagens, interaction)
            embed= await view.update_message(interaction)
            imagem = await view.imagem()
            res = await view.deletar_arquivo()
            print(f"AÇÃO : {res}")
            await interaction.response.send_message(view=view, embed=embed, file=imagem)
        else:
            await interaction.response.send_message("Nenhum personagem encontrado")

async def setup(bot):
    await bot.add_cog(Personagens(bot))
