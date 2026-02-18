import discord
from discord.ext import commands
from discord.ext.commands.core import has_role, has_permissions

import random

class general(commands.Cog):
    # constructor
    def __init__(self, client):
        self.client= client

    #1. Return Latency of bot
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("{0} ms".format(round(self.client.latency * 1000)))


    #2. Hello command
    @commands.command()
    async def hello(self, ctx):
        await ctx.message.reply(f'Hey {ctx.author.mention}! Wassup?')


    #3. Purge command
    @commands.command()
    @has_permissions(manage_messages= True)
    async def clear(self, ctx, amount = 4):
        await ctx.channel.purge(limit = amount + 1)


    #4. Ask a question from bot
    @commands.command()
    async def ask(self, ctx, *, question):
        responses = ['Yes', 'No', 'Ummm...Yes', 'Ummm...No', 'Ummm...Maybe', 'Definately', 'No doubt', 'Forget it', 'Yaas']
        await ctx.message.reply(random.choice(responses))


    #5. Help command
    @commands.command()
    @has_role('DUSC Bot Admin')
    async def help(self, ctx):
        prefix= await self.client.get_prefix(ctx.message)
        space= '\u200b'
        helpEmbed= discord.Embed(   title="Help is Here",
                                    description= "",
                                    color= discord.Colour.blue())
        
        helpEmbed.add_field(name= f"{prefix}ping",
                            value= "Returns latency of the bot.",
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}clear",
                            value= "Purge command, with default limit= 5.",
                            inline=True)
        helpEmbed.add_field(name= space,
                            value= space,
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}hello",
                            value= "Hello Command.",
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}ask",
                            value= "Ask a Yes/No question from bot.",
                            inline=True)
        helpEmbed.add_field(name= space,
                            value= space,
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}setflag",
                            value= "To set value of flag for refresh command",
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}setid",
                            value= "To set id of guild/channel/logs/course/club",
                            inline=True)
        helpEmbed.add_field(name= space,
                            value= space,
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}course",
                            value= "Send course embed with menu",
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}club",
                            value= "Send club embed with menu",
                            inline=True)
        helpEmbed.add_field(name= space,
                            value= space,
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}refresh",
                            value= "To manually refresh the menus",
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}loadnews",
                            value= "Loads spotlight news from website",
                            inline=True)
        helpEmbed.add_field(name= space,
                            value= space,
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}setch",
                            value= "Set channel for sending new announcements",
                            inline=True)
        helpEmbed.add_field(name= f"{prefix}dumpdb",
                            value= "Dump the json Database file",
                            inline=True)
        helpEmbed.add_field(name= space,
                            value= space,
                            inline=True)

        await ctx.send(embed= helpEmbed)



def setup(client):
  client.add_cog(general(client))
