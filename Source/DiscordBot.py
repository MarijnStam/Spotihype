from msilib.schema import Error
import discord
from discord.ext import commands
import os
from dotenv import find_dotenv, load_dotenv

import WebScaper as wb
import Spotify as sp

#Load our enviroment variables 
load_dotenv(find_dotenv())
TOKEN               = os.getenv('DISCORD_TOKEN')
FORUM_CHANNEL_ID    = os.getenv('DISCORD_FORUM_CHANNEL')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    #Singleton variables for interacting with the discord server
    global channel

    print('We have logged in as {0.user}'.format(bot))
    channel = bot.get_channel(int(FORUM_CHANNEL_ID))

@bot.command(
	help="Prints a list of all albums in a playlist",
	brief="Prints a list of all albums in a playlist"
)
async def listAlbums(ctx):
	await ctx.send("List of some albums")

@bot.command(
help="Add albums (from static list for now) to your AOTY playlist",
args="Amount: Number of albums you want to add. 1-20"
brief="Adds albums to your list"
)
async def addAlbums(ctx, arg: int = 5):

    #Sanity check the input
    if not isinstance(arg, int):
        await ctx.send(f"Please enter the amount of albums to add as a number")

    amount = int(arg)
    if((amount <= 0) or (amount >= 21)):
        await ctx.send(f"Please enter a valid range between 0 - 20")
        return

    albumList = wb.getAlbums()

    for album in albumList:
        print(album)
        uri = sp.getAlbumURI(album)
        sp.addAlbumToPlaylist(uri, sp.AOTY_PLAYLIST_ID)
        #TODO Add some extra info instead of just the name here. Maybe Embed with img
        await ctx.send(f"Added: {album}")
    


def startBot():
    print("Starting bot")
    try:
        bot.run(TOKEN)
    except Error as e:
        print("Aah!")