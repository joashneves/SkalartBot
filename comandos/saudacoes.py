import discord
from discord.ext import commands
from datetime import datetime
from models import Obter_Usuario
from models.Obter_dia import Manipular_dia
import random
import pytz


class MonitorarSaudacoes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fuso_brasilia = pytz.timezone("America/Sao_Paulo")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignora mensagens de bots
        id_discord = str(message.author.id)
        conteudo = message.content.lower()
        # Obtém a data e hora no fuso de Brasília
        agora = datetime.now(self.fuso_brasilia)
        hora_atual = agora.hour
        dia_atual = agora.date()
        # Gera moedas e xp aleatórios
        moedas_ganhas = random.randint(1, 5)  # Gera entre 10 e 50 moedas
        xp_ganho = random.randint(10, 50)  # Gera entre 1 e 3 xp

        # Verifica se o usuário deu bom dia ou boa noite
        if "bom dia" in conteudo:
            print(dia_atual)
            if hora_atual < 12:  # Permite dar bom dia somente antes das 12h
                bomdia = Manipular_dia.obter_bomdia(message.author.id)
                if bomdia:
                    if bomdia["data_bomdia"].date() != dia_atual:
                        Manipular_dia.registrar_bomdia(message.author.id)
                        await message.channel.send(
                            f"Bom dia, {message.author.mention}!"
                        )
                    else:
                        return
                else:
                    # Se for a primeira vez, registra e confirma
                    Manipular_dia.registrar_bomdia(message.author.id)
                    await message.channel.send(f"Bom dia, {message.author.mention}!")
            else:
                await message.channel.send(f"Já passou das 12h!")
                return
            usuario_registrado = Obter_Usuario.Manipular_Usuario.obter_usuario(
                id_discord
            )
            if usuario_registrado:
                usuario_atualizado = Obter_Usuario.Manipular_Usuario.adicionar_moedas(
                    id_discord, moedas_ganhas
                )
                usuario_atualizado = Obter_Usuario.Manipular_Usuario.adicionar_xp(
                    id_discord, xp_ganho
                )
                print(usuario_atualizado)

        elif "boa noite" in conteudo:
            print(dia_atual)
            if hora_atual >= 18:  # Permite dar boa noite somente depois das 18h
                boanoite = Manipular_dia.obter_boanoite(message.author.id)
                if boanoite:
                    if boanoite["data_boanoite"].date() != dia_atual:
                        print(boanoite["data_boanoite"], dia_atual)
                        Manipular_dia.registrar_boanoite(message.author.id)
                        await message.channel.send(f"Boa noite")
                    else:
                        return
                else:
                    Manipular_dia.registrar_boanoite(message.author.id)
                    await message.channel.send(f"Boa noite, {message.author.mention}!")
            else:
                await message.channel.send(f"Ainda não é noite")
                return
            usuario_registrado = Obter_Usuario.Manipular_Usuario.obter_usuario(
                id_discord
            )
            if usuario_registrado:
                usuario_atualizado = Obter_Usuario.Manipular_Usuario.adicionar_moedas(
                    id_discord, moedas_ganhas
                )
                usuario_atualizado = Obter_Usuario.Manipular_Usuario.adicionar_xp(
                    id_discord, xp_ganho
                )
                print(usuario_atualizado)


async def setup(bot: commands.Bot):
    await bot.add_cog(MonitorarSaudacoes(bot))
