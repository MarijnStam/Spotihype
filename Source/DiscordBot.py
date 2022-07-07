import discord
from discord.ext import commands
import os
from dotenv import find_dotenv, load_dotenv
import sqlite3

import WebScaper as wb
import Spotify as sp
import db

#Load our enviroment variables 
load_dotenv(find_dotenv())
TOKEN               = os.getenv('DISCORD_TOKEN')
FORUM_CHANNEL_ID    = os.getenv('DISCORD_CHANNEL')
TESTING_CHANNEL_ID = os.getenv('DISCORD_TESTING_CHANNEL_ID')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    #Singleton variables for interacting with the discord server
    global channel
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.embeds[0].fields[0].name == "Like / Dislike? React to this message with:":
        if reaction.emoji == "👍":
            await reaction.message.channel.send("You liked the album! Moving to liked playlist")
            await reaction.message.delete()

        elif reaction.emoji == "👎":
            await reaction.message.channel.send("You disliked the album, removing from playlist")
            await reaction.message.delete()
        
        else:
            await reaction.message.channel.send("Keeping this album in the playlist for now")
            await reaction.message.delete()

@bot.command(
    help="Prints a list of all albums in a playlist",
    brief="Prints a list of all albums in a playlist"
)
async def review(ctx):
    albums = sp.getPlaylistTracks(sp.AOTY_PLAYLIST_ID)
    for album in albums:
        embed=discord.Embed(
            title=f"{album.artist} - {album.name}",
            url=f"{album.link}",
            color=discord.Color.blue())
        embed.set_thumbnail(url=album.img)
        embed.add_field(name="Like / Dislike? React to this message with:", value=":thumbsup: / :thumbsdown:")
        await ctx.send(embed=embed)

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

    playlistName, playlistLink = sp.getPlaylist(sp.AOTY_PLAYLIST_ID)
    
    index = 0
    addedAlbumCount = 0

    while (addedAlbumCount < amount):
        #Retrieve the spotify album from the artist/album info from the webscraper. add the entry to the local db 
        try:
            album = sp.Album(albumList[index])
        except sp.NotFoundError as e:
            print(e)
            continue

        #Try adding album details to db
        try:            
            db.addAlbum(album.artist, album.name, album.uri)
            sp.addAlbumToPlaylist(album.uri, sp.AOTY_PLAYLIST_ID)
            addedAlbumCount = addedAlbumCount + 1
        #If we encounter this error, it means the ID is already in the db, skip this album and increment amount to add
        except sqlite3.Error as e: 
            continue

        finally:
            index = index + 1

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
