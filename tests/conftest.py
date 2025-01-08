import pytest_asyncio
import discord
from discord.ext import commands
import discord.ext.test as dpytest

@pytest_asyncio.fixture
async def bot():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix="$", intents=intents)
    dpytest.configure(b)
    return b

@pytest_asyncio.fixture(autouse=True)
async def cleanup():
    yield
    await dpytest.empty_queue()

