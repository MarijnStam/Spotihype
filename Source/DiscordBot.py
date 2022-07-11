import discord
from discord import app_commands
from discord import ui
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
TESTING_CHANNEL_ID  = os.getenv('DISCORD_TESTING_CHANNEL_ID')
GUILD_ID            = os.getenv('DISCORD_GUILD')

GUILD = discord.Object(id=GUILD_ID)

class SpotihypeBot(discord.Client):
    """Class for the bot itself, subclasses `discord.Client`

    Parameters
    ----------
    intents : `discord.Intents`
        Needed intents for the bot
    
    Attributes
    ----------
    tree : `app_commands.CommandTree`
        The command tree for the bot
    """    
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
        print('We have logged in as {0.user}'.format(bot))

class EmbedButton(ui.Button):
    """Class for creating a Discord button component

    Attributes
    ----------
    callback : optional
        Callback for the button event, by default `None`
    """
    def __init__(self, callback=None, **kwargs):
        #Init the button with kwargs elements
        super().__init__(**kwargs)
        if callback is not None:
            self.callback = callback
        
class Paginator(ui.View):
    """Class for creating a Discord paginator View to scroll through a list of Embeds

    Parameters
    ----------
    embedList : `list`
        List of embeds to paginate through

    Attributes
    ----------
    embedList : `list`
        List of embeds to paginate through
    index : `int`
        Index of the current embed

    Methods (callbacks only, not intended to be called directly)
    ----------
    `__left(self, interaction: discord.Interaction, button: ui.Button)`
        Callback when left button is pressed
    `__right(self, interaction: discord.Interaction, button: ui.Button)`
        Callback when right button is pressed
    """ 
    def __init__(self, embedList: list):     
        super().__init__()
        self.embedList = embedList
        self.index = 0
        #Create the paginator buttons, pass the callbacks defined in this class
        self.add_item(EmbedButton(callback=self.__left, emoji="⬅", disabled=True, custom_id="left"))
        self.add_item(EmbedButton(label=f"0 / {len(embedList) - 1}", custom_id="index", disabled=True))
        #Disable the paginator all together if we only have a single embed
        if len(embedList) > 1:
            self.add_item(EmbedButton(callback=self.__right, emoji="➡", custom_id="right"))
        else:
            self.add_item(EmbedButton(callback=self.__right, emoji="➡", disabled=True, custom_id="right"))

    #Callback function for the right button
    async def __right(self, interaction: discord.Interaction):
        """Callback for the paginate right button. Scrolls the paginator right
        and updates the index of the counter.

        Parameters
        ----------
        interaction : `discord.Interaction`
            The discord interaction event that triggered the callback
        """    
        #Disable the button when we have reached the last index
        if self.index == len(self.embedList) - 2:
            self.children[2].disabled=True
            self.index += 1
        elif self.index < len(self.embedList) - 1:
            self.index += 1
        else:
            return
    
        #Set the left button disabled to False since we have scrolled right
        #Update the index of the counter
        self.children[0].disabled = False
        self.children[1].label = f"{self.index} / {len(self.embedList) - 1}"

        await interaction.response.edit_message(embed=self.embedList[self.index],view=self)

    async def __left(self, interaction: discord.Interaction):            
        """Callback for the paginate left button. Scrolls the paginator left
        and updates the index of the counter.

        Parameters
        ----------
        interaction : `discord.Interaction`
            The discord interaction event that triggered the callback
        """    
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
        self.children[1].label = f"{self.index} / {len(self.embedList) - 1}"

        await interaction.response.edit_message(embed=self.embedList[self.index],view=self)

class ReviewButtons(ui.View):
    """Class for creating a Review view. Creates 3 buttons with callbacks for actions

    Parameters
    ----------
    paginator : `Paginator`
        The paginator object for this View, used to get the index and list of embeds

    Attributes
    ----------
    paginator : `Paginator`
        The paginator object for this View, used to get the index and list of embeds

    Methods (callbacks only, not intended to be called directly)
    ----------
    `__delete(self, interaction: discord.Interaction)`
        Callback when delete button is pressed, album will be deleted from AOTY list
    `__save(self, interaction: discord.Interaction)`
        Callback when save button is pressed, album will be moved from AOTY list to saved list
    `__review(self, interaction: discord.Interaction)`
        Callback when review button is pressed, user will be prompted for an album review
    """    
    # Define the actual buttons
    def __init__(self, paginator: Paginator):
        super().__init__()
        #Add the paginator to this view
        self.paginator = paginator
        self.add_item(EmbedButton(callback=self.__delete, label="Delete", style=discord.ButtonStyle.danger, row=1))
        self.add_item(EmbedButton(callback=self.__save, label="Save", style=discord.ButtonStyle.success, row=1))
        self.add_item(EmbedButton(callback=self.__review, label="Review", style=discord.ButtonStyle.primary, row=1))

    async def __delete(self, interaction: discord.Interaction):
        """Callback on delete button press. Deletes the album from the AOTY list

        Parameters
        ----------
        interaction : discord.Interaction
            Interaction of the button press event
        """        
        albumURI = self.paginator.embedList[self.paginator.index].url.rsplit('/', 1)[-1]
        self.paginator.embedList[self.paginator.index].title = "DELETED"
        self.paginator.embedList[self.paginator.index].color = discord.Color.red()
        sp.deleteAlbum(albumURI, sp.AOTY_PLAYLIST_ID)
        await interaction.response.edit_message(embed=self.paginator.embedList[self.paginator.index])

    async def __save(self, interaction: discord.Interaction):
        """Callback on save button press. Saves the album to the saved list

        Parameters
        ----------
        interaction : discord.Interaction
            Interaction of the button press event
        """   
        albumURI = self.paginator.embedList[self.paginator.index].url.rsplit('/', 1)[-1]
        self.paginator.embedList[self.paginator.index].title = "SAVED"
        self.paginator.embedList[self.paginator.index].color = discord.Color.green()
        sp.moveAlbum(albumURI, sp.AOTY_PLAYLIST_ID, sp.LIKED_PLAYLIST_ID)
        await interaction.response.edit_message(embed=self.paginator.embedList[self.paginator.index])
        
    async def __review(self, interaction: discord.Interaction):
        """Callback on review button press. Prompts the user for an album review

        Parameters
        ----------
        interaction : discord.Interaction
            Interaction of the button press event
        """   
        print("Review")

class AddButtons(ui.View):
    """Class for creating an Add Albums view

    Parameters
    ----------
    paginator : `Paginator`
        The paginator object for this View, used to get the index and list of embeds

    Attributes
    ----------
    paginator : `Paginator`
        The paginator object for this View, used to get the index and list of embeds

    Methods (callbacks only, not intended to be called directly)
    ----------
    `__delete(self, interaction: discord.Interaction)`
        Callback when delete button is pressed, album will be deleted from AOTY list
    `__replace(self, interaction: discord.Interaction)`
        Callback when replacebutton is pressed, album will be removed from AOTY list and replaced by another
    """    
    # Define the actual buttons
    def __init__(self, paginator: Paginator):
        super().__init__()
        #Add the paginator to this view
        self.paginator = paginator
        self.add_item(EmbedButton(callback=self.__delete, label="Delete", style=discord.ButtonStyle.danger, row=1))
        self.add_item(EmbedButton(callback=self.__replace, label="Replace", style=discord.ButtonStyle.primary, row=1))


    async def __delete(self, interaction: discord.Interaction):
        """Callback on delete button press. Deletes the album from the AOTY list

        Parameters
        ----------
        interaction : discord.Interaction
            Interaction of the button press event
        """        
        albumURI = self.paginator.embedList[self.paginator.index].url.rsplit('/', 1)[-1]
        self.paginator.embedList[self.paginator.index].title = "DELETED"
        self.paginator.embedList[self.paginator.index].color = discord.Color.red()
        sp.deleteAlbum(albumURI, sp.AOTY_PLAYLIST_ID)
        await interaction.response.edit_message(embed=self.paginator.embedList[self.paginator.index])

    async def __replace(self, interaction: discord.Interaction):
        """Callback on replace button press. Album will be removed and replaced by another

        Parameters
        ----------
        interaction : discord.Interaction
            Interaction of the button press event
        """   
        # albumURI = self.paginator.embedList[self.paginator.index].url.rsplit('/', 1)[-1]
        # self.paginator.embedList[self.paginator.index].title = "SAVED"
        # self.paginator.embedList[self.paginator.index].color = discord.Color.green()
        # await interaction.response.edit_message(embed=self.paginator.embedList[self.paginator.index])
        print("Replace")

intents = discord.Intents.default()
bot = SpotihypeBot(intents=intents)

@bot.tree.command(description="Review albums in the AOTY playlist")
async def review(interaction: discord.Interaction):
    """Review command which sends a paginated list of Embeds to the user.
    The user can scroll through the list and perform actions on the albums.

    Parameters
    ----------
    interaction : `discord.Interaction`
        The interaction event that triggered the command. Contains the context
    """    
    albums = sp.getPlaylistAlbums(sp.AOTY_PLAYLIST_ID)
    embedList = []

    #Iterate through the albums retrieved and construct an Embed for each one
    #Appends the embed to the embedList
    for album in albums:
        embed=discord.Embed(
            title="Album Review",
            url=f"{album.link}",
            color=discord.Color.blue())

        embed.set_thumbnail(url=album.img)
        embed.add_field(name="Album", value=album.name, inline=False)
        embed.add_field(name="Artist", value=album.artist, inline=False)
        embedList.append(embed)
        
    #Construct a paginator view with the embedList
    url_view = Paginator(embedList)

    #Add the review buttons to the view, send the response
    reviewButtons = ReviewButtons(url_view)
    for item in reviewButtons.children: 
            url_view.add_item(item)
    await interaction.response.send_message(embed=embedList[0], view=url_view)

@bot.tree.command(description="Add album to AOTY playlist")
@app_commands.describe(
    amount='Amount of albums to add',
)
async def add(interaction: discord.Interaction, amount: int = 5):
    """Add command which adds albums to the AOTY playlist.

    Parameters
    ----------
    interaction : `discord.Interaction`
        The interaction event that triggered the command. Contains the context
    amount : `int`, optional
        amount of albums to add, by default 5
    """
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

#TODO Probably move this functionality away from this command so it can be tested
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
            title="Album Added",
            url=f"{album.link}",
            color=discord.Color.green())
        embed.set_thumbnail(url=album.img)
        embed.add_field(name="Album", value=album.name, inline=False)
        embed.add_field(name="Artist", value=album.artist, inline=False)
        embed.set_footer(text="Retrieved from highest-rated/2022")
        embedList.append(embed)
    
    #Construct a paginator view with the embedList
    view = Paginator(embedList)

    addButtons = AddButtons(view)
    for item in addButtons.children:
        view.add_item(item)

    await interaction.followup.send(embed=embedList[0], view=view)
    

def startBot():
    """Starts the Discord bot with a static token
    """    
    print("Starting bot")
    bot.run(TOKEN)
