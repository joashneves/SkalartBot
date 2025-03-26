import discord
from discord import app_commands
from discord.ext import commands
import requests
import json
import aiohttp
import hashlib
import os

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
    def __init__(self, id, name,  timeout = None):
        super().__init__(timeout=timeout)
        self.id = id
        self.name = name
        self.caminho = None

    async def get_embed(self):
        caminho_arquivo = await self.imagem()

        embed = discord.Embed(
            title=f"Personagem: {self.name}",
            description="Franquia: ",
            color=discord.Color.blue(),
        )
        embed.set_image(url=f"attachment://image.jpg")
        print(caminho_arquivo)
        embed.set_footer(text="Api utilizada")
        return embed

    async def imagem(self):
        caminho_arquivo = await carrega_imagem(f"https://personagensaleatorios.squareweb.app/api/Personagems/DownloadPersonagemByName?nome={self.name}&franquia=")
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



class Game(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot


    @commands.command()
    async def req(self, ctx):
        req = requests.get("https://personagensaleatorios.squareweb.app/api/Personagems")
        content = json.loads(req.content)
        print(content["id"])
        view = PersonagensView(content["id"], content["name"])
        embed = await view.get_embed()
        imagem = await view.imagem()
        await ctx.send(embed=embed, file=imagem)
        res = await view.deletar_arquivo()
        print(res)


async def setup(bot):
    await bot.add_cog(Game(bot))
