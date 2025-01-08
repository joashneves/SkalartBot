import discord.ext.test as dpytest
import pytest

@pytest.mark.cogs("general")
async def test_ping_command(bot):
    """Testa o comando $ping"""
    dpytest.message("$ping")
    assert dpytest.verify().message().content("Pong!")
