import discord
from discord.ext import commands
from discord.ext.commands.core import has_role, has_permissions
from discord.errors import NotFound, Forbidden

import json

# class for handeling Database
class jsdb:
    #0. constructor
    def __init__(self):
        self._cacheddata= {}
        self.reload()

    #1. dump data in json file
    def dumpdata(self):
        with open("cogs/_cache/cache.json", "w") as wf:
            json.dump(self._cacheddata, wf, indent=6)
            print("log: Wrote data in json file")
        self.reload()

    #2. reload data from json file
    def reload(self):
        with open("cogs/_cache/cache.json", "r") as rf:
            self._cacheddata= json.load(rf)
            print("log: Reloaded the database into dictionary")


# class for building rolemenus
class MySelect(discord.ui.Select):
    #0. constructor
    def __init__(self, _guild, opts= []):
        self.guild= _guild
        options= opts
        super().__init__(
          placeholder='Click to Select',
          min_values=0,
          max_values=len(options),
          options=options)
    
    #1. function to respond when user interacts with the menu
    async def callback(self, interaction):
        if not self.values:
            # await interaction.response.send_message(interaction.user.mention)
            await interaction.response.send_message(
                f"{interaction.user.mention} You haven't chosen anything, Please choose an option!",
                ephemeral=True)
        
        else:
            for optionselected in self.values:
                if optionselected == "Geography" or optionselected == "Geology":
                    optionselected= "Geography | Geology"

                if optionselected == "Mathematics" or optionselected == "Statistics":
                    optionselected= "Math & Stats"
                
                # fetch role for selected option
                try:
                    optionrole: discord.Role = discord.utils.get(
                                                self.guild.roles, name= optionselected)
                    # await interaction.send(courserole.mention)

                except NotFound:
                    await interaction.response.send_message(
                        f'{optionselected} Role not found',
                        ephemeral=True)
                    continue
                    
                else:
                    # assign role to the user
                    try:
                        await interaction.user.add_roles(optionrole)
                        print(interaction.user, optionrole)

                    except Forbidden:
                        await interaction.response.send_message(
                            f"{interaction.user.mention} I am missing permissions to assign roles! Please contact admin",
                            ephemeral=True)
                        continue
                    else:
                        await interaction.response.send_message(
                            f"{interaction.user.mention} You have chosen {self.values}",
                            ephemeral=True)


# class for handeling rolemenus
class rolemenu(commands.Cog):
    #0. constructor
    def __init__(self, client):
        self.client= client
        self._jsdb_class= jsdb()

        self.courseoptions= []
        self.cluboptions= []
        
        self._guild= None

        # loading options from the json file
        self.f_loadopts()

    #1. function to load options from json Database
    def f_loadopts(self):
        _courseopts= self._jsdb_class._cacheddata["courseopts"]
        _clubopts= self._jsdb_class._cacheddata["clubopts"]

        for opt in _courseopts:
            self.courseoptions.append(
                discord.SelectOption(label=opt, value=opt)
            )
        for opt in _clubopts:
            self.cluboptions.append(
                discord.SelectOption(label=opt, value=opt)
            )

    #2. function to set flag value
    def f_setflag(self, boolval : bool):
        self._jsdb_class._cacheddata["flag"]= boolval
        self._jsdb_class.dumpdata()
        
        return self._jsdb_class._cacheddata["flag"]

    #3. function to reinitialize the menu whenever bot restarts
    async def f_refresh(self):
        _guild= await self.client.fetch_guild(
            self._jsdb_class._cacheddata["Idcache"]["guildId"])
        _channel= await _guild.fetch_channel(
            self._jsdb_class._cacheddata["Idcache"]["channelId"])
        _logschannel= await self.client.fetch_channel(
            self._jsdb_class._cacheddata["Idcache"]["logschannelId"])

        _coursemessage= await _channel.fetch_message(
            self._jsdb_class._cacheddata["Idcache"]["messageId"]["course"])
        _clubmessage= await _channel.fetch_message(
            self._jsdb_class._cacheddata["Idcache"]["messageId"]["club"])
        
        _interaction= _coursemessage.components
        del _interaction
        _interaction= _clubmessage.components
        del _interaction

        view = discord.ui.View(timeout= None)
        view.add_item(MySelect(_guild, opts=self.courseoptions))
        await _coursemessage.edit(view= view)
        await _logschannel.send(f"Reinitialized {_coursemessage.id} with new menu")
        print(f"Reinitialized course {_coursemessage.id} with new menu")

        del view

        view = discord.ui.View(timeout= None)
        view.add_item(MySelect(_guild, opts=self.cluboptions))
        await _clubmessage.edit(view= view)
        await _logschannel.send(f"Reinitialized {_clubmessage.id} with new meny")
        print(f"Reinitialized club {_clubmessage.id} with new menu")

    #1. on_ready event for refresh command whenever bot restarts
    @commands.Cog.listener()
    async def on_ready(self):
        self.f_setflag(True)
        if(self._jsdb_class._cacheddata["flag"]):
            await self.f_refresh()
        else:
            pass
    
    #2. command to overwrite flag value in Database
    @commands.command()
    @has_permissions(administrator=True)
    async def setflag(self, ctx, val= 't'):
        result= None
        if val == 't':
            result= self.f_setflag(boolval= True)
        else:
            result= self.f_setflag(boolval= False)

        await ctx.message.reply(f"Flag Set to {result}")

    #3. command to overwrite Idcache in Database
    @commands.command()
    @has_permissions(administrator=True)
    async def setid(self, ctx, _type= "", _id= None):
        # overwrite id in dictionary
        if _type == "guild":
            self._jsdb_class._cacheddata["Idcache"]["guildId"]= _id
        elif _type == "channel":
            self._jsdb_class._cacheddata["Idcache"]["channel"]= _id
        elif _type == "logs":
            self._jsdb_class._cacheddata["Idcache"]["logschannelId"]= _id
        elif _type == "course":
            self._jsdb_class._cacheddata["Idcache"]["messageId"]["course"]= _id
        elif _type == "club":
            self._jsdb_class._cacheddata["Idcache"]["messageId"]["club"]= _id
        else:
            await ctx.message.reply(f"{ctx.author.mention} Please enter a valid id")
            return
        
        await ctx.message.reply(f"{ctx.author.mention} Set {_type} to {_id}")
        # write data in Database
        self._jsdb_class.dumpdata()

    #4. course menu
    @commands.command()
    @has_permissions(administrator=True)
    async def course(self, ctx):
        self.f_setflag(True)
        _guild= await self.client.fetch_guild(
                        self._cacheDataclass._cacheddata["Idcache"]["guildId"])

        interface_embed= discord.Embed(
            title= 'Course Menu',
            description= "",
            colour= discord.Colour.green())

        interface_embed.add_field(  
            name= "Choose your subjects from the menu below.",
            value= """Choose the subject(s) related to your course and get access   to that subject's chatroom.

                    - You can choose any number of subjects.
                    
                    - Students of any language course (English, Hindi, Sanskrit...) choose "Language".

                    - If on desktop/laptop choose your subject and click anywhere outside the screen.

                    - If you have any query, you can ask  <@780453103173632011>, <@672077825938817045> or  <@706694432610844724>
                    """,
            inline= False)

        view = discord.ui.View(timeout= None)
        view.add_item(MySelect(self._guild, opts=self.courseoptions))

        message= await ctx.send(embed= interface_embed, view= view)

        
        self._jsdb_class._cacheddata["Idcache"]["messageId"]["course"]= message.id
        print("course: ", 
            self._cacheDataclass._cacheddata["Idcache"]["messageId"]["course"])
        self._cacheDataclass.dumpdata()

    #5. club menu
    @commands.command()
    @has_permissions(administrator=True)
    async def club(self, ctx):
        self.f_setflag(True)
        _guild= await self.client.fetch_guild(
                        self._cacheDataclass._cacheddata["Idcache"]["guildId"])

        interface_embed= discord.Embed(
            title= 'Club Menu',
            description= "",
            colour= discord.Colour.green())

        interface_embed.add_field(  
            name= "Join clubs that from the menu below.",
            value= """There are multiple clubs in the server, you can join any as per your interests.
                    - If on desktop/laptop choose your club and click anywhere outside the screen.

                    - If you have any query, you can ask <@780453103173632011>, <@672077825938817045> or <@706694432610844724>
                    
                    :AwOo: Anime

                    :performing_arts: Artist

                    :computer: Coding

                    :money_with_wings: Finance

                    :video_game: Gaming
                    
                    :projector: Movie

                    :musical_note: Music

                    :book: Reading

                    :gear:- Science & Tech
                    """,
            inline= False)

        view = discord.ui.View(timeout= None)
        view.add_item(MySelect(self._guild, opts=self.cluboptions))

        message= await ctx.send(embed= interface_embed, view= view)

        self._cacheDataclass._cacheddata["Idcache"]["messageId"]["club"]= message.id
        print("club: ", 
            self._cacheDataclass._cacheddata["Idcache"]["messageId"]["club"])
        self._cacheDataclass.dumpdata()

    #6. command to manually refresh interactions
    @commands.command()
    async def refresh(self, ctx):
        await self.f_refresh()

def setup(client):
  client.add_cog(rolemenu(client))
