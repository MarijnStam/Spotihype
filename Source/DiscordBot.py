from subprocess import call
import discord
from discord import app_commands
from discord import ui
import os
from dotenv import find_dotenv, load_dotenv
import sqlite3
import traceback

import WebScaper as wb
import Spotify as sp
import db

#Load our enviroment variables 
load_dotenv(find_dotenv())
TOKEN               = os.getenv('DISCORD_TOKEN')
FORUM_CHANNEL_ID    = os.getenv('DISCORD_CHANNEL')
TESTING_CHANNEL_ID  = os.getenv('DISCORD_TESTING_CHANNEL_ID')
GUILD_ID            = os.getenv('DISCORD_GUILD')

GUILD = discord.Object(id=GUILD_ID)

class SpotihypeBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

class EmbedButton(ui.Button):
    """Class for creating a discord button

    Args:
        ui.Button: Button needs to be subclassed
    """
    def __init__(self, callback=None, **kwargs):
        #Init the button with kwargs elements
        super().__init__(**kwargs)
        if callback is not None:
            self.callback = callback
        
class Paginator(ui.View):
    """Class for making a paginator for the album list

    Args:
        ui.View: View needs to be subclassed
    """
    def __init__(self, albumList: list):
        super().__init__()
        self.albumList = albumList
        self.index = 0
        #Create the paginator buttons, pass the callbacks defined in this class
        self.add_item(EmbedButton(callback=self.left, emoji="⬅", disabled=True, custom_id="left"))
        self.add_item(EmbedButton(label=f"0 / {len(albumList) - 1}", custom_id="index", disabled=True))
        self.add_item(EmbedButton(callback=self.right, emoji="➡", custom_id="right"))

    #Callback function for the right button
    async def right(self, interaction: discord.Interaction):

        #Disable the button when we have reached the last index
        if self.index == len(self.albumList) - 2:
            self.children[2].disabled=True
            self.index += 1
        elif self.index < len(self.albumList) - 1:
            self.index += 1
        else:
            return
    
        #Set the left button disabled to False since we have scrolled right
        #Update the index of the counter
        self.children[0].disabled = False
        self.children[1].label = f"{self.index} / {len(self.albumList) - 1}"

        await interaction.response.edit_message(embed=self.albumList[self.index],view=self)

    async def left(self, interaction: discord.Interaction):            

        #Disable the button when we have reached the first index
        if self.index == 1:
            self.children[0].disabled=True
            self.index -= 1
        elif self.index > 0:
            self.index -= 1
        else:
            return
        
        #Set the right button disabled to False since we have scrolled left
        #Update the index of the counter
        self.children[2].disabled = False
        self.children[1].label = f"{self.index} / {len(self.albumList) - 1}"

        await interaction.response.edit_message(embed=self.albumList[self.index],view=self)

class ReviewButtons(ui.View):
    # Define the actual button
    def __init__(self):
        super().__init__()

    @ui.button(label="Delete", style=discord.ButtonStyle.danger, row=1)
    async def delete(self, interaction: discord.Interaction, button: ui.Button):
        print("Delete")

    @ui.button(label="Save", style=discord.ButtonStyle.success, row=1)
    async def save(self, interaction: discord.Interaction, button: ui.Button):
        print("Save")

    @ui.button(label="Review", style=discord.ButtonStyle.secondary, row=1)
    async def review(self, interaction: discord.Interaction, button: ui.Button):
        print("Review")
    
intents = discord.Intents.default()
bot = SpotihypeBot(intents=intents)

@bot.event
async def on_ready():
    #Singleton variables for interacting with the discord server
    global channel
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_reaction_add(reaction, user):
    #Is the reaction to the proper message in case of review?
    if reaction.message.embeds[0].fields[0].name == "Like / Dislike? React to this message with:":
        #If so, parse the URI and the name of the album
        albumURI = reaction.message.embeds[0].url.rsplit('/', 1)[-1]
        albumName = reaction.message.embeds[0].title

        #Handle operations based on added emoji
        if reaction.emoji == "👍":
            await reaction.message.delete()
            await reaction.message.channel.send(f"You liked **{albumName}**! Moving to liked playlist")
            sp.moveAlbum(albumURI, sp.AOTY_PLAYLIST_ID, sp.LIKED_PLAYLIST_ID)

        elif reaction.emoji == "👎":
            await reaction.message.delete()
            await reaction.message.channel.send(f"You disliked **{albumName}**, removing from playlist")
            sp.deleteAlbum(albumURI, sp.AOTY_PLAYLIST_ID)

        else:
            await reaction.message.delete()
            await reaction.message.channel.send(f"Keeping **{albumName}** in the playlist for now")        


@bot.tree.command(description="Review albums in the AOTY playlist")
async def review(interaction: discord.Interaction):
    albums = sp.getPlaylistTracks(sp.AOTY_PLAYLIST_ID)
    embedList = []
    #Embedlist supports up to 10 albums
    for index, album in zip(range(10), albums):
        embed=discord.Embed(
            title="Album Review",
            url=f"{album.link}",
            color=discord.Color.blue())

        embed.set_thumbnail(url=album.img)
        embed.add_field(name="Album", value=album.name, inline=False)
        embed.add_field(name="Artist", value=album.artist, inline=False)
        embedList.append(embed)
        
    url_view = Paginator(albumList=embedList)
    reviewButtons = ReviewButtons()
    for item in reviewButtons.children: 
        url_view.add_item(item)
    await interaction.response.send_message(embed=embedList[0], view=url_view)

@bot.tree.command(description="Add album to AOTY playlist")
@app_commands.describe(
    amount='Amount of albums to add',
)
async def add(interaction: discord.Interaction, amount: int = 5):

    amount = int(amount)
    if((amount <= 0) or (amount >= 21)):
        await interaction.response.send_message(f"Please enter a valid range between 0 - 20")
        return

    await interaction.response.defer(thinking=True)

    albumList = wb.getAlbums()
    playlistName, playlistLink = sp.getPlaylist(sp.AOTY_PLAYLIST_ID)
    
    index = 0
    addedAlbumCount = 0
    embedList = []

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

        embed=discord.Embed(
        title=f"{album.artist} - {album.name}",
            url=f"{album.link}",
            color=discord.Color.green())
        embed.set_thumbnail(url=album.img)
        embed.add_field(name="Added to playlist", value=f"[{playlistName}]({playlistLink})")
        #TODO Make dynamic
        embed.set_footer(text="Retrieved from highest-rated/2022")
        embedList.append(embed)

    await interaction.followup.send(embeds=embedList)
    

def startBot():
    print("Starting bot")
    bot.run(TOKEN)
