import discord
from discord import app_commands
from discord.ext import commands
import requests
import json
import aiohttp
import hashlib
import os
import time

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
    def __init__(self, id, name, gender, franquia, timeout = None):
        super().__init__(timeout=timeout)
        self.id = id
        self.name = name
        self.gender = gender
        self.franquia = franquia
        self.caminho = None

    async def get_embed(self):
        caminho_arquivo = await self.imagem()

        embed = discord.Embed(
            title=f"Personagem: {self.name}",
            description=f"Franquia: {self.franquia} \n Genero: {self.gender}",
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
        self.mensagem = []

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.mensagem:
            if self.mensagem[5] == message.author.id and self.mensagem[1] == message.channel.id:
                if message.content.lower() == self.mensagem[3].lower():
                    await message.channel.send("Voce acertou!")
                    self.mensagem = []
                else:
                    self.mensagem[6] = self.mensagem[6] - 1
                    await message.channel.send(f"Voce errou! Agora voce só tem {self.mensagem[6]} tentativas")
                if self.mensagem[6] <= 0 or self.mensagem[4] == False:
                    self.mensagem = []
                print(self.mensagem)
            else:
                print(f"{message.author.id}Pessoa não é {self.mensagem[5]} ou/e não esta no canal certo")

    @commands.command()
    async def jogar(self, ctx):
        if not self.mensagem:
            req = requests.get("https://personagensaleatorios.squareweb.app/api/Personagems")
            content = json.loads(req.content)
            print(content["franquia"]["name"])
            view = PersonagensView(content["id"], content["name"], content["gender"], content["franquia"]["name"])
            embed = await view.get_embed()
            imagem = await view.imagem()
            msg = await ctx.send(embed=embed, file=imagem)
            print("mensaem", msg)
            res = await view.deletar_arquivo()
            print(res)
            self.mensagem = [ msg.id, msg.channel.id, msg.guild.id, content["name"], True, ctx.author.id, 5]
            print(self.mensagem)
        else:
            await ctx.send("um jogo ja esta em andamento")

    @jogar.error
    async def command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"command is on cooldown",description=f"Try again in {error.retry_after:.2f}s.", color=0xFFFF00)
            await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Game(bot))
