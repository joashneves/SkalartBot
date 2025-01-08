import pytest_asyncio
import discord
from discord.ext import commands
import discord.ext.test as dpytest

@pytest_asyncio.fixture
async def test_bot_ready(bot):
    """Teste básico para verificar o estado inicial do bot."""
    await bot.on_ready()
    assert bot.user is None  # Apenas para validar o funcionamento inicial
