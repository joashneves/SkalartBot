import sys
import os
import pytest
import asyncio

# Ajusta o caminho para encontrar o bot
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bot')))
print("socorro")

# Agora você pode importar os módulos do bot
from bot.main import bot

# Função para verificar se o bot está online (já conectado)
async def verificar_bot_online():
    # Verifica se o bot está pronto para interagir com o Discord
    if not bot.is_ready():
        raise Exception("Bot não está online!")
    return f"Bot {bot.user.name} está online!"

@pytest.mark.asyncio
async def test_bot_ready():
    print("Teste Iniciado")
    # Aguarda o bot estar online
    await verificar_bot_online()
    print("Bot está online e pronto!")

    # Agora você pode rodar seus testes no bot
    # Adicione os testes necessários aqui
    # Exemplo: Verificar se o comando de ping está funcionando

    # Envia uma mensagem simulada de ping (supondo que você tenha um comando $ping no bot)
    await dpytest.message("$ping")

    # Verifica a resposta
    assert dpytest.verify().message().content("Pong!")
    print("Comando $ping foi respondido corretamente!")
