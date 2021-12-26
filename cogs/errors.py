import discord
from discord.ext import commands

class errors(commands.Cog):
    def __init__(self, client):
        self.client= client
    
    @commands.Cog.listener()
    async def on_error(self,on_ready):
        print('An error in firing up the bot.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed= discord.Embed(title= 'Error : Please pass in all the required arguments', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)

        #not working
        elif isinstance(error, commands.TooManyArguments):
            error_embed= discord.Embed(title= 'Error : Too many arguments', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)
            
        elif isinstance(error, commands.MissingPermissions):
            error_embed= discord.Embed(title= 'Error : You don\'t have the requred permissions to use this command', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)
            
        elif isinstance(error, commands.BotMissingPermissions):
            error_embed= discord.Embed(title= 'Error : I don\'t have the required permissions to use this command', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)
            
        elif isinstance(error, commands.ChannelNotFound):
            error_embed= discord.Embed(title= 'Error : Could\'t find the mentioned channel', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)
        
        elif isinstance(error, commands.ChannelNotReadable):
            error_embed= discord.Embed(title= 'Error : I don\'t have permissions to read messages in the mentioned channel', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)

        elif isinstance(error, commands.CommandNotFound):
            error_embed= discord.Embed(title= 'Error : The bot does not have this command', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)
            
        elif isinstance(error, commands.CommandOnCooldown):
            error_embed= discord.Embed(title= f'Error : This command is on cooldown. Please try after {round((error.retry_after)/60)} min', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)
            
        elif isinstance(error, commands.MissingRole):
            error_embed= discord.Embed(title= 'Error : You are missing the required role to use this command', description= "", colour= discord.Colour.red())
            await ctx.send(embed= error_embed)

        elif isinstance(error, commands.DisabledCommand):
            error_embed= discord.Embed(title= 'Error : This command in disabled in this guild', description= "", Color= discord.Color.red())
            await ctx.send(embed= error_embed)

        elif isinstance(error, commands.UserNotFound):
            error_embed= discord.Embed(title= 'Error : Couldn\'t find the mentioned user', description= "", Color= discord.Color.red())
            await ctx.send(embed= error_embed)

        elif isinstance(error, commands.MessageNotFound):
            error_embed= discord.Embed(title= 'Error : Message not found', description= "", Color= discord.Color.red())
            await ctx.send(embed= error_embed)
        
        elif isinstance(error, commands.NotOwner):
            error_embed= discord.Embed(title= 'Error : This is an owner only command', description= "", Color= discord.Color.red())
            await ctx.send(embed= error_embed)

        else:
            await ctx.send(f"Out Error: {error}")

def setup(client):
  client.add_cog(errors(client))
