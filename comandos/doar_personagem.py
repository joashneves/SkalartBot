import discord
from discord import app_commands
from discord.ext import commands
import models
from models.Obter_personagem import Manipular_Personagem
class DoarPersonagem(commands.Cog):
    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="doar_personagem", description="Troca um personagem com alguem")
    @app_commands.describe(nome="Nome do personagem que voce quer enviar")
    @app_commands.describe(franquia="Nome da franquia que voce quer enviar o personagem")
    @app_commands.describe(user="usuario que voce quer enviar o personagem")
    async def doar_personagem(self, interaction: discord.Interaction,
                                  nome: str,
                                  franquia: str,
                                  user: discord.Member):
        personagem = Manipular_Personagem.Obeter_um_personagem(interaction.guild.id, nome, franquia)
        if not personagem:
            return
        await interaction.response.send_message(f"{nome}, {franquia}, {user}, {personagem}")

    @doar_personagem.autocomplete('nome')
    async def doar_personagem_autocomplete(self,interact: discord.Interaction, pesquisa:str):
        print(pesquisa)
        opcaoes = []
        personas = Manipular_Personagem.obter_todos_personagens_descoberto_usuario(interact.user.id, interact.guild.id)
        for sonas in personas:
            sonas_option = app_commands.Choice(name=f"{sonas.nome_personagem}", value=f"{sonas.nome_personagem}")
            opcaoes.append(sonas_option)
        return opcaoes

    @doar_personagem.autocomplete('franquia')
    async def doar_personagem_autocomplete_franquia(self,interact: discord.Interaction, pesquisa:str):
        print(pesquisa)
        opcaoes = []
        personas = Manipular_Personagem.obter_todos_personagens_descoberto_usuario(interact.user.id, interact.guild.id)
        franquias = []
        for franquia in personas:
            print(franquias)
            if not franquia.franquia_personagem in franquias:
                franquias.append(franquia.franquia_personagem)
        for sonas in franquias:
            sonas_option = app_commands.Choice(name=f"{sonas}", value=f"{sonas}")
            opcaoes.append(sonas_option)
        return opcaoes


async def setup(bot):
    await bot.add_cog(DoarPersonagem(bot))
