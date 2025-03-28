import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from asyncio import TaskGroup
import models
from models.Obter_personagem import Manipular_Personagem
class DoarPersonagem(commands.Cog):
    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot
        self.troca = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        print(f"VAR : {self.troca}")
        if message.author.id in self.troca:
            id_dono_novo = message.author.id
            if self.troca[message.author.id] != []:
                if message.content.startswith("sim"):
                    await message.channel.send("A troca foi aceita")
                    Manipular_Personagem.alterar_dono_personage(self.troca[id_dono_novo][0],
                        self.troca[id_dono_novo][1],
                        self.troca[id_dono_novo][2],
                        self.troca[id_dono_novo][3],
                        self.troca[id_dono_novo][4],
                        self.troca[id_dono_novo][5])
                    del self.troca[message.author.id]
                    await message.channel.send("Personagem trocado!")
                elif message.content.startswith("não"):
                    await message.channel.send("A troca foi recusada")
                    del self.troca[message.author.id]
                    print(f"VAR : {self.troca}")
                else:
                    print("MSG : Mensagem não é de troca")

    async def temporizador(self, msg, id_novo_dono, interaction,  sleeptime):
        print(f"AVISO : temporizador iniciado com {sleeptime} segundos e self.mensagem {self.troca[id_novo_dono]}")
        await asyncio.sleep(sleeptime)
        if id_novo_dono in self.troca:
            if self.troca[id_novo_dono] == []:
                return
            del self.troca[id_novo_dono] 
            await interaction.response.send_message("acabou o tempo de troca")



    @app_commands.command(name="doar_personagem", description="Troca um personagem com alguem")
    @app_commands.describe(nome="Nome do personagem que voce quer enviar")
    @app_commands.describe(franquia="Nome da franquia que voce quer enviar o personagem")
    @app_commands.describe(user="usuario que voce quer enviar o personagem")
    async def doar_personagem(self, interaction: discord.Interaction,
                                  nome: str,
                                  franquia: str,
                                  user: discord.Member):
        personagem = Manipular_Personagem.Obter_um_personagem(interaction.guild.id, nome, franquia)
        id_dono_antigo = interaction.user.id
        id_dono_novo = user.id
        guild_id = interaction.guild.id
        print(f"VAR : {user.id} == {interaction.user.id}")
        if user.id == interaction.user.id:
            await interaction.response.send_message("Não é possivel enviar um personagem para voce mesmo")
            return
        if not personagem:
            return
        await interaction.response.send_message(f"Troca iniciada, responda com sim ou não{nome}, {franquia}, {user}, {personagem}")
        msg = interaction.id
        self.troca[id_dono_novo] = ([id_dono_novo, id_dono_antigo, guild_id, personagem.id_personagem, nome, franquia ])
        print(f"VAR : {self.troca[id_dono_novo]}")
        async with TaskGroup() as group:
            group.create_task(self.temporizador(msg, id_dono_novo, interaction, 26))


    @doar_personagem.autocomplete('nome')
    async def doar_personagem_autocomplete(self,interact: discord.Interaction, pesquisa:str):
        opcaoes = []
        personas = Manipular_Personagem.obter_todos_personagens_descoberto_usuario(interact.user.id, interact.guild.id)
        for sonas in personas:
            sonas_option = app_commands.Choice(name=f"{sonas.nome_personagem}", value=f"{sonas.nome_personagem}")
            opcaoes.append(sonas_option)
        return opcaoes

    @doar_personagem.autocomplete('franquia')
    async def doar_personagem_autocomplete_franquia(self,interact: discord.Interaction, pesquisa:str):
        opcaoes = []
        personas = Manipular_Personagem.obter_todos_personagens_descoberto_usuario(interact.user.id, interact.guild.id)
        franquias = []
        for franquia in personas:
            if not franquia.franquia_personagem in franquias:
                franquias.append(franquia.franquia_personagem)
        for sonas in franquias:
            sonas_option = app_commands.Choice(name=f"{sonas}", value=f"{sonas}")
            opcaoes.append(sonas_option)
        return opcaoes


async def setup(bot):
    await bot.add_cog(DoarPersonagem(bot))
