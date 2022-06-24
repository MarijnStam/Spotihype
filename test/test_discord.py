import pytest
import discord.ext.test as dpytest
import discord
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from Source import DiscordBot

@pytest.fixture
def bot(event_loop):
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix='!', intents=intents, loop=event_loop)
    dpytest.configure(bot)
    return bot

# @pytest.mark.asyncio
# async def test_ping(bot):
#     await dpytest.message(channel=DiscordBot.TESTING_CHANNEL_ID, content="!ping")
#     assert dpytest.verify().message().contains().content("Ping:")

@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("!ping")
    assert dpytest.verify().message().contains().content("Ping:")