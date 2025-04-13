import discord
from discord import app_commands
from discord.ext import commands
import requests
import json
import aiohttp
import hashlib
import os
import asyncio
from asyncio import TaskGroup
from datetime import datetime
import random
from models.Obter_personagem import Manipular_Personagem
from models.Obter_Usuario import Manipular_Usuario

IMAGENS_DIR = "imagens_temp"
os.makedirs(IMAGENS_DIR, exist_ok=True)
NUM_JOGADAS = {}

async def reset_num_jogadas(id_player, sleeptime):
    await asyncio.sleep(sleeptime)
    if not NUM_JOGADAS:
            NUM_JOGADAS[id_player] = ([id_player, 10, False])
    else:
        if id_player in NUM_JOGADAS:
            if NUM_JOGADAS[id_player][0] == id_player:
                NUM_JOGADAS[id_player][1] = NUM_JOGADAS[id_player][1] - 1
            if NUM_JOGADAS[id_player][1] != 0 and NUM_JOGADAS[id_player][2] == False:
                NUM_JOGADAS[id_player][2] = True
                print(f"resetou : ", id_player)
                NUM_JOGADAS[id_player] = ([id_player, 10, False])
        else:
            NUM_JOGADAS[id_player] = ([id_player, 10, False])
    return NUM_JOGADAS[id_player]


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
            title=f"Adivinhe o personagem",
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
        self.mensagem = {}
        self.delymensagem = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        try:
            if message.channel.id in self.mensagem:
                print(f"VAR : menssagem guild id {message.channel.id}")
                print(f"VAR : self.mensagem[id] : {self.mensagem[message.channel.id]}")
                if  self.mensagem[message.channel.id] != []:
                    if self.mensagem[message.channel.id][5] == message.author.id and self.mensagem[message.channel.id][1] == message.channel.id:
                        if message.content.lower() in ["ff", "desisto!"]:
                            del self.mensagem[message.channel.id]
                            await message.channel.send(f"Voce desistiu!")
                        if message.content.lower() == self.mensagem[message.channel.id][3].lower():
                            await message.channel.send("Voce acertou!")
                            id_usuario_string = str(message.author.id)
                            usuario = Manipular_Usuario.obter_usuario(id_usuario_string)
                            if usuario:
                                xp = random.randint(15, 25)
                                dinheiro = random.randint(50, 70)
                                Manipular_Usuario.adicionar_xp(id_usuario_string, xp )
                                Manipular_Usuario.adicionar_moedas(id_usuario_string, dinheiro)
                                print(f"AÇÃO : Moedas {dinheiro} e xp {xp} adicionadas ao {usuario.id_discord}")
                            print(f"PROMPT : {message.guild.id, self.mensagem[message.channel.id][3], self.mensagem[message.channel.id][9]}")
                            personagem = Manipular_Personagem.Obter_um_personagem(message.guild.id, self.mensagem[message.channel.id][3], self.mensagem[message.channel.id][9])
                            if not personagem:
                                Manipular_Personagem.salvar_personagem(str(message.author.id),
                                                                    message.guild.id,
                                                                    message.channel.id,
                                                                    self.mensagem[message.channel.id][7],
                                                                    self.mensagem[message.channel.id][3],
                                                                    self.mensagem[message.channel.id][8],
                                                                    self.mensagem[message.channel.id][9],
                                                                    self.mensagem[message.channel.id][10],
                                                                    datetime.now()
                                                                        )
                                await message.channel.send(f"{self.mensagem[message.channel.id][3]} agora é seu!")
                            elif personagem.id_discord == message.author.id:
                                print(f"VAR : {personagem.id_discord == message.author.id}")
                                await message.channel.send("Voce ja possui esse personagem.")
                            else:
                                await message.channel.send(f"{self.mensagem[message.channel.id][3]} Ja pertence a alguem!")
                            del self.mensagem[message.channel.id]
                        elif self.mensagem[message.channel.id][6] <= 0:
                            del self.mensagem[message.channel.id]
                            await message.channel.send(f"Voce perdeu")
                        else:
                            await message.channel.send(f"Voce errou! Agora voce só tem {self.mensagem[message.channel.id][6]} tentativas")
                            self.mensagem[message.channel.id][6] = self.mensagem[message.channel.id][6] - 1
                    else:
                        print(f"ID : {message.author.id} Pessoa não é {self.mensagem[message.channel.id][5]} ou/e não esta no canal certo")
        except Exception as e:
            print(f"Aviso de error : {e}")

    async def temporizador(self, msg, channel_id, id_mensagem, sleeptime):
        print(f"AVISO : temporizador iniciado com {sleeptime} segundos , e self.mensagem {self.mensagem[channel_id]}")
        await asyncio.sleep(sleeptime)
        print(f"AVISO : Saiu do temporizador")
        if channel_id in self.mensagem:
            if not id_mensagem in self.mensagem[channel_id]:
                return
            if self.mensagem[channel_id] == []:
                return
            print(f"o jogo do {id_mensagem}")
            del self.mensagem[channel_id]
            await msg.send("acabou o jogo")


    @commands.command()
    @commands.cooldown(1, 9, commands.BucketType.user)
    async def jogar(self, ctx):
        id_player = ctx.author.id
        try:
            if id_player in NUM_JOGADAS and NUM_JOGADAS[id_player][1] <= 0:
                await ctx.send("Quantidade de adivinhação vencida tente novamenteo mais tarde", ephemeral=True)
                return

            if ctx.channel.id in self.delymensagem:
                await ctx.send("Alguem ja esta jogando", ephemeral=True)
                return
            else:
                self.delymensagem[ctx.channel.id] = ctx.author.id


            if not ctx.channel.id in self.mensagem or self.mensagem[ctx.channel.id] == []:
                if not NUM_JOGADAS:
                    NUM_JOGADAS[id_player] = ([id_player, 10, False])

                if not id_player in NUM_JOGADAS:
                    NUM_JOGADAS[id_player] = ([id_player, 10, False])


                if NUM_JOGADAS[ctx.author.id][1] > 0:
                    print(f" VAR : Numenro de tentativas {NUM_JOGADAS}")
                    await ctx.send(f"carregando a imagem, aguarde... voce tem {NUM_JOGADAS[id_player][1]} jogadas")
                    req = requests.get("https://personagensaleatorios.squareweb.app/api/Personagems")
                    print(req)
                    content = json.loads(req.content)
                    print(content["franquia"]["name"])
                    view = PersonagensView(content["id"], content["name"], content["gender"], content["franquia"]["name"])
                    embed = await view.get_embed()
                    imagem = await view.imagem()
                    msg = await ctx.send(embed=embed, file=imagem)
                    print("VAR : mensagem = ", msg)
                    res = await view.deletar_arquivo()
                    print(res)
                    del self.delymensagem[ctx.channel.id]
                    self.mensagem[msg.channel.id] = ([ msg.id, msg.channel.id, msg.guild.id, content["name"], True, ctx.author.id, 5, content["id"], content["gender"], content["franquia"]["name"], content["caminhoArquivo"]])
                    async with TaskGroup() as group:
                        try:
                            if msg.channel.id in self.mensagem:
                                tesk = group.create_task(self.temporizador(ctx, msg.channel.id, msg.id, 26))
                                if tesk:
                                    tesk.cancel()
                                    group.create_task(self.temporizador(ctx, msg.channel.id, msg.id, 26))                     
                            print(f"VAR : nova self.mensagem = {self.mensagem}")
                            if NUM_JOGADAS[ctx.author.id][1] == 10:
                                group.create_task(reset_num_jogadas(ctx.author.id, 60*30))
                            NUM_JOGADAS[ctx.author.id][1] = NUM_JOGADAS[ctx.author.id][1] - 1
                        except asyncio.CancelledError:
                            print("ALARM : Event loop was cancelled")
                        except Exception as e:
                            print(f"AVISO ERROR : {e}")
                else:
                    await ctx.send("Quantidade de adivinhação vencida tente novamenteo mais tarde", ephemeral=True)

            else:
                await ctx.send("um jogo ja esta em andamento", ephemeral=True)
        except Exception as e:
            print(f"AVISO DE ERROR : Error em $jogar {e}")
            await ctx.send("Ocorreu um erro ")

    @jogar.error
    async def jogar_error(self, ctx, err):
        if isinstance(err, commands.errors.CommandOnCooldown):
            tentativa = err.retry_after
            tentativa
            await ctx.reply(f'Comando esta em cooldown para voce, tente novamente em {round(tentativa, 2)} segundos', ephemeral=True)
            print(f"AVISO DE ERROR : {tentativa}")

        print(f"AVISO DE ERROR : {err}")
        

async def setup(bot):
    await bot.add_cog(Game(bot))
