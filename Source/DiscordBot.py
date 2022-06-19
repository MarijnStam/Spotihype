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
brief="Adds albums to your list"
)
async def addAlbums(ctx, arg: int = 5):
    
    amount = int(arg)
    if((amount <= 0) or (amount >= 21)):
        await ctx.send(f"Please enter a valid range between 0 - 20")
        return

    albumList = wb.getAlbums()

    for i in range(0, amount):
        album = sp.Album(albumList[i])
        sp.addAlbumToPlaylist(album.uri, sp.AOTY_PLAYLIST_ID)
        playlistName, playlistLink = sp.getPlaylist(sp.AOTY_PLAYLIST_ID)

#MAKE INTO ONE BIG EMBED INSTEAD, TOO MUCH GOING ON
        embed=discord.Embed(
        title=f"{album.artist} - {album.name}",
            url=f"{album.link}",
            color=discord.Color.green())
        embed.set_thumbnail(url=album.img)
        embed.add_field(name="Added to playlist", value=f"[{playlistName}]({playlistLink})")
        #TODO Make dynamic
        embed.set_footer(text="Retrieved from highest-rated/2022")

        await ctx.send(embed=embed)
    


def startBot():
    print("Starting bot")
    bot.run(TOKEN)
