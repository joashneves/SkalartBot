import discord
from discord.ext import commands
from datetime import datetime
from models.Obter_dia import Manipular_dia

class MonitorarSaudacoes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignora mensagens de bots

        conteudo = message.content.lower()
        hora_atual = datetime.now().hour  # Obtém a hora atual
        dia_atual = datetime.now()

        # Verifica se o usuário deu bom dia ou boa noite
        if 'bom dia' in conteudo:
            if hora_atual < 12:  # Permite dar bom dia somente antes das 12h
                bomdia = Manipular_dia.obter_bomdia(message.author.id)
                if bomdia:
                    if bomdia["data_bomdia"] != dia_atual:
                        Manipular_dia.registrar_bomdia(message.author.id)
                        await message.channel.send(f"Bom dia, {message.author.mention}! Você já disse bom dia {bomdia['numero_bomdia'] + 1} vezes.")
                else:
                    # Se for a primeira vez, registra e confirma
                    Manipular_dia.registrar_bomdia(message.author.id)
                    await message.channel.send(f"Bom dia, {message.author.mention}!")
            else:
                await message.channel.send(f"Você não pode mais dar bom dia, {message.author.mention}. Já passou das 12h!")

        elif 'boa noite' in conteudo:
            if hora_atual >= 18:  # Permite dar boa noite somente depois das 18h
                boanoite = Manipular_dia.obter_boanoite(message.author.id)
                if boanoite:
                        if boanoite["data_boanoite"] != dia_atual:
                            Manipular_dia.registrar_boanoite(message.author.id)
                            await message.channel.send(f"Você já deu boa noite, {message.author.mention}, e não pode dar outra boa noite hoje.")
                else:
                    Manipular_dia.registrar_boanoite(message.author.id)
                    await message.channel.send(f"Boa noite, {message.author.mention}!")
            else:
                await message.channel.send(f"Você não pode dar boa noite agora, {message.author.mention}. Só é permitido após às 18h!")

async def setup(bot: commands.Bot):
    await bot.add_cog(MonitorarSaudacoes(bot))
